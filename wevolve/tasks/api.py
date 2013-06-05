import json

from django.conf.urls.defaults import url
from django.http import HttpResponse
from django.forms.models import model_to_dict

from tastypie.resources import ALL
from tastypie import fields
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.authentication import (Authentication, MultiAuthentication,
                                     SessionAuthentication)
from tastypie.utils import now, trailing_slash

from wevolve.tasks.models import Task, TaskSkill, TaskUser
from wevolve.projects.api import ProjectPartResource
from wevolve.libs.generic_resource import (GenericResource, GenericMeta,
                                           ActivityGenericResource)
from wevolve.libs.serializers import DateSerializer
from wevolve.project_parts.authorization import ProjectPartElemAuthorization
from wevolve.users.api import UserResource
from wevolve.tasks.validation import TaskValidation
from wevolve.libs.oauthauthentication import OAuth20Authentication


class TaskResource(ActivityGenericResource):
    project_part = fields.ForeignKey(ProjectPartResource, 'project_part')
    created_user = fields.ForeignKey(UserResource, 'created_user',
                                     readonly=True)
    created = fields.DateTimeField(attribute='created',
                                   readonly=True, null=True)
    modified = fields.DateTimeField(attribute='modified',
                                    readonly=True, null=True)
    user = fields.ForeignKey(UserResource, 'user', null=True)

    # Relations
    comments = fields.ToManyField('wevolve.project_parts.api.CommentResource',
                                  'comment_set',
                                  full=True,
                                  null=True)
    username = fields.CharField(readonly=True)

    # Others
    project_title = fields.CharField(readonly=True,
                                     attribute='project_part__project__title')
    project_part_title = fields.CharField(readonly=True,
                                          attribute='project_part__title')
    url = fields.CharField(readonly=True)

    class Meta(GenericMeta):
        list_allowed_methods = ['get', 'post', 'patch', 'put']
        queryset = Task.objects.all()
        resource_name = 'task'
        filtering = {'project_part': ALL, 'user': ALL, 'flag_finished': ALL}
        serializer = DateSerializer()
        validation = TaskValidation()
        authorization = ProjectPartElemAuthorization()
        authentication = MultiAuthentication(OAuth20Authentication(),
                                             SessionAuthentication(),
                                             Authentication())

    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/order%s$"
                    % (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('task_order'), name="api_task_order")
                ]

    def task_order(self, request, **kwargs):
        tasks = sorted(json.loads(request.raw_post_data)['objects'], key=lambda x: x['id'])
        task_objects = Task.objects.filter(pk__in=map(lambda x: x['id'], tasks))
        task_list = zip(tasks, task_objects)

        for task, task_object in task_list:
            task_object.weight = task['weight']
            task_object.save()

        bundles = [self.build_bundle(model_to_dict(task_object),
                                     request=request)
                   for task_object in task_objects]

        return self.create_response(request, bundles)

    def obj_create(self, bundle, **kwargs):
        created = now()
        return super(TaskResource, self).obj_create(bundle,
                                                    created=created,
                                                    created_user=bundle.request.user)

    def dehydrate_username(self, bundle):
        if bundle.obj.user:
            return " ".join([bundle.obj.user.first_name,
                            bundle.obj.user.last_name])
        else:
            return ""

    def dehydrate_url(self, bundle):
        return bundle.obj.get_absolute_url()
