import json

from django.forms.models import model_to_dict
from django.conf.urls.defaults import url
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from tastypie.resources import ALL
from tastypie import fields
from tastypie.authentication import (Authentication, MultiAuthentication,
                                     SessionAuthentication)
from tastypie.utils import trailing_slash

from wevolve.libs.generic_resource import GenericResource, GenericMeta, ActivityGenericResource
from wevolve.projects.authorization import ProjectAuthorization, ProjectPartAuthorization
from wevolve.projects.models import Project, ProjectPart, UserProject
from wevolve.users.api import UserResource
from wevolve.projects.validation import ProjectValidation, ProjectPartValidation
from wevolve.libs.drive_service import DriveUtil, update_drive_folder
from wevolve.libs.oauthauthentication import OAuth20Authentication


class ProjectResource(GenericResource):
    image_name = fields.CharField(attribute='image_name',
                                  readonly=True, null=True)
    image_original_name = fields.CharField(attribute='image_original_name',
                                           readonly=True, null=True)
    licence = fields.IntegerField(attribute='licence',
                                  readonly=True, null=True)
    created = fields.DateTimeField(attribute='created',
                                   readonly=True, null=True)
    modified = fields.DateTimeField(attribute='modified',
                                    readonly=True, null=True)
    type_field = fields.IntegerField(attribute='type_field', null=True)

    # Relations
    project_parts = fields.ListField()
    members = fields.ListField()
    current_user = fields.IntegerField(readonly=True)
    user_permission = fields.IntegerField(readonly=True)
    categories = fields.ToManyField('wevolve.home.api.CategoryResource',
                                    'categories',
                                    null=True, full=True)
    # Other fields
    maxmin = fields.ListField()

    class Meta(GenericMeta):
        queryset = Project.objects.all()
        resource_name = 'project'
        authentication = MultiAuthentication(OAuth20Authentication(),
                                             SessionAuthentication(),
                                             Authentication(),
                                             )
        authorization = ProjectAuthorization()
        validation = ProjectValidation()

    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/invite%s$"
                    % (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('invite'), name="project_invite"),
                url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/uninvite%s$"
                    % (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('uninvite'), name="project_uninvite"),
                url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/change_perms%s$"
                    % (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('change_perms'), name="project_change_perms")
                ]

    def invite(self, request, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        data = json.loads(request.raw_post_data)
        if not 'user' in data:
            return HttpResponse('Unauthorized', status=401)
        user = get_object_or_404(User, pk=data['user'])

        if UserProject.objects.check_perms(project, request.user):
            user_project = UserProject(project=project, user=user,
                                       permission=0, created_user=request.user)
            user_project.save()
            response_data = {'id': user.id,
                             'user': '/api/v1/user/%d/' % user.id,
                             'username': ' '.join([user.first_name, user.last_name]),
                             'permission': 0}
        else:
            return HttpResponse('Unauthorized', status=401)

        return HttpResponse(json.dumps(response_data),
                            mimetype='application/json')

    def uninvite(self, request, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        data = json.loads(request.raw_post_data)
        user = get_object_or_404(User, pk=data['user'])

        if UserProject.objects.check_perms(project, request.user):
            userproject = UserProject.objects.get(project=project, user=user)
            userproject.delete()
            response_data = {'status': 'ok'}
        else:
            return HttpResponse('Unauthorized', status=401)

        return HttpResponse(json.dumps(response_data),
                            mimetype='application/json')

    def change_perms(self, request, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        data = json.loads(request.raw_post_data)
        user = get_object_or_404(User, pk=data['user'])

        # Changing perms
        if UserProject.objects.check_perms(project, request.user):
            userproject = UserProject.objects.get(project=project, user=user)
            userproject.permission = data['permission']
            userproject.save()
            response_data = {'status': 'ok'}
        else:
            return HttpResponse('Unauthorized', status=401)

        return HttpResponse(json.dumps(response_data),
                            mimetype='application/json')

    def dehydrate_current_user(self, bundle):
        user = bundle.request.user
        if user.is_authenticated():
            return user.id
        else:
            return None

    def dehydrate_user_permission(self, bundle):
        return bundle.obj.get_user_permission(bundle.request.user)

    def dehydrate_maxmin(self, bundle):
        return bundle.obj.get_maxmin_activity()

    def dehydrate_project_parts(self, bundle):
        if bundle.request.GET.get('network', None) or\
           bundle.obj.get_user_permission(bundle.request.user) is False and\
           bundle.obj.type_field != 0:
            return []

        project_part_bundles = []
        project_parts = bundle.obj.projectpart_set.all()
        for project_part in project_parts:
            project_part_aux = model_to_dict(project_part)
            project_part_aux = {'id': project_part_aux['id'],
                                'title': project_part_aux['title'],
                                'project_part': project_part_aux['project_part'],
                                'project': project_part_aux['project'],
                                'progress': project_part.progress(),
                                'progress_done': project_part.progress_done(),
                                'task_count': project_part.task_count(),
                                'has_drive': project_part.has_drive()
                                }
            project_part_bundles.append(project_part_aux)

        return project_part_bundles

    def dehydrate_members(self, bundle):
        userprojects = [userproject for userproject in bundle.obj.userproject_set.all()]
        bundles = []
        for userproject in userprojects:
            user = userproject.user
            user_aux = model_to_dict(user)
            user_aux = {'id': user.id,
                        'user': '/api/v1/user/%d/' % user.id,
                        'username': ' '.join([user.first_name, user.last_name]),
                        'permission': userproject.permission,
                        'projects': user.profile.projects(bundle.request.user)
                        }
            bundles.append(self.build_bundle(data=user_aux, request=bundle.request))
        return bundles

    def dehydrate_image_name(self, bundle):
        return bundle.obj.get_image_name()

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ProjectResource, self).build_filters(filters)

        if 'open' in filters:
            projects = Project.objects.filter(type_field=0)
            orm_filters['pk__in'] = [u.pk for u in projects]

        return orm_filters

    def obj_create(self, bundle, **kwargs):
        result = super(ProjectResource, self).obj_create(bundle,
                                                         created_user=bundle.request.user)
        user_project = UserProject(project=bundle.obj, user=bundle.request.user,
                                   permission=1, created_user=bundle.request.user)
        user_project.save()
        project_part = ProjectPart(title='Project Part 1', project=bundle.obj,
                                   order=0, created_user=bundle.request.user)
        project_part.save()
        return result

    def obj_update(self, bundle, **kwargs):
        # FIXME Workaround for the annoying updates of foreign keys in tastypie
        if '/project/' in bundle.request.path and bundle.request.user.is_authenticated():
            old_project = Project.objects.get(pk=kwargs['pk'])
            if 'title' in bundle.data and bundle.data['title'] != old_project.title:
                update_drive_folder(old_project,
                                    bundle.data['title'], bundle.request.user)
        return super(ProjectResource, self).obj_update(bundle,
                                                       **kwargs)


class ProjectPartResource(ActivityGenericResource):
    project = fields.IntegerField('project__id', null=True)
    project_part = fields.IntegerField(attribute='project_part__id', null=True)
    order = fields.IntegerField(readonly=True, null=True, blank=True)
    created_user = fields.ToOneField(UserResource, 'created_user',
                                     readonly=True)
    created = fields.DateTimeField(attribute='created',
                                   readonly=True, null=True)
    modified = fields.DateTimeField(attribute='modified',
                                    readonly=True, null=True)
    # Relations
    project_part_id = fields.ToOneField('self', 'project_part', null=True)
    project_id = fields.ToOneField(ProjectResource, 'project')

    # Other fields
    progress = fields.IntegerField(readonly=True)
    progress_done = fields.IntegerField(readonly=True)
    task_count = fields.IntegerField(readonly=True)
    has_drive = fields.BooleanField()
    has_viewed = fields.BooleanField()

    class Meta(GenericMeta):
        queryset = ProjectPart.objects.all()
        resource_name = 'project_part'
        filtering = {'project': ALL}
        validation = ProjectPartValidation()
        authentication = MultiAuthentication(SessionAuthentication(), Authentication())
        authorization = ProjectPartAuthorization()

    def dehydrate_progress(self, bundle):
        return bundle.obj.progress()

    def dehydrate_progress_done(self, bundle):
        return bundle.obj.progress_done()

    def dehydrate_task_count(self, bundle):
        return bundle.obj.task_count()

    def dehydrate_has_drive(self, bundle):
        return bundle.obj.has_drive()

    def dehydrate_has_viewed(self, bundle):
        if not bundle.request.user.is_authenticated():
            return False
        user_token = bundle.request.user.profile.drive_token
        if bundle.obj.drive_id and user_token:
            f = DriveUtil(user_token).get_file(bundle.obj.drive_id)
            if f:
                return f['labels']['viewed']
        return False

    def obj_create(self, bundle, **kwargs):
        return super(ProjectPartResource, self).obj_create(bundle,
                                                           created_user=bundle.request.user)

    def obj_update(self, bundle, **kwargs):
        # FIXME Workaround for the annoying updates of foreign keys in tastypie
        if '/project_part/' in bundle.request.path and bundle.request.user.is_authenticated():
            old_project_part = ProjectPart.objects.get(pk=kwargs['pk'])
            if 'title' in bundle.data and bundle.data['title'] != old_project_part.title:
                update_drive_folder(old_project_part,
                                    bundle.data['title'], bundle.request.user)
        return super(ProjectPartResource, self).obj_update(bundle,
                                                           **kwargs)
