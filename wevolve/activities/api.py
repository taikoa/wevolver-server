import logging

from django.db.models import Q
from django.contrib.auth.models import User
from tastypie.resources import ALL
from tastypie import fields
from tastypie.authentication import (Authentication, MultiAuthentication,
                                     SessionAuthentication)

from wevolve.libs.generic_resource import GenericResource, GenericMeta
from wevolve.activities.models import Activity
from wevolve.libs.serializers import MomentSerializer
from wevolve.projects.models import ProjectPart


class ActivityResource(GenericResource):
    username = fields.CharField(readonly=True)
    project_part_title = fields.CharField('project_part__title')
    project_title = fields.CharField('project_part__project__title')
    url = fields.CharField(null=True, readonly=True)
    comment_data = fields.DictField(readonly=True)

    class Meta(GenericMeta):
        queryset = Activity.objects.all()
        filtering = {'project_part': ALL,
                     'user': ALL
                     }
        serializer = MomentSerializer()
        allowed_methods = ['get']
        authentication = MultiAuthentication(SessionAuthentication(), Authentication())

    def dehydrate_action(self, bundle):
        return bundle.obj.get_action_name()

    def dehydrate_url(self, bundle):
        return bundle.obj.get_url()

    def dehydrate_comment_data(self, bundle):
        return bundle.obj.get_comment_data()

    def dehydrate_username(self, bundle):
        return ' '.join([bundle.obj.user.first_name,
                        bundle.obj.user.last_name])

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(ActivityResource, self).build_filters(filters)

        if "project" in filters:
            project_parts = ProjectPart.objects.filter(project__id=filters['project'])
            orm_filters['project_part__in'] = project_parts

        return orm_filters

    def get_object_list(self, request):
        current_user = request.user
        user_id = request.GET.get('user', None)
        project_id = request.GET.get('project', None)
        object_list = super(ActivityResource, self).get_object_list(request)

        if user_id:
            if current_user.is_authenticated():
                projects = [user_project.project.id for user_project in current_user.userproject_set.all()]
            else:
                try:
                    user = User.objects.get(pk=user_id)
                    projects = [user_project.project.id for user_project in user.userproject_set.all()]
                except User.DoesNotExist:
                    projects = []
                    logging.error('No user with id %s' % user_id)

            if current_user.is_authenticated() and current_user.id == int(user_id):
                # Own Profile
                object_list = object_list.filter(Q(user__id=user_id)
                                                 | Q(project_part__project__in=projects))
            else:
                object_list = object_list.filter(Q(user__id=user_id)
                                                 & (Q(project_part__project__type_field=0)
                                                 | Q(project_part__project__in=projects)))
        elif project_id:
            object_list = object_list.filter(Q(project_part__project__id=project_id)
                                             & (Q(user__id=current_user.id) | Q(project_part__project__type_field=0)))
        return object_list.order_by('-created')

    def obj_create(self, bundle, **kwargs):
        return super(GenericResource, self).obj_create(bundle, user=bundle.request.user)
