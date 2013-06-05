import re
import string

from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource

from wevolve.project_parts.models import Comment, Post
from wevolve.projects.models import ProjectPart
from wevolve.tasks.models import Task
from wevolve.activities.models import Activity


class GenericResource(ModelResource):
    def determine_format(self, request):
        """
           Necessary to avoid the format=json
           attribute in the url
        """
        return 'application/json'


class ActivityGenericResource(GenericResource):
    def alter_detail_data_to_serialize(self, request, data):
        if request.method == 'POST':
            Activity.objects.set_activity('add', data.obj)
        elif request.method == 'PUT':
            Activity.objects.set_activity('update', data.obj)

        return super(ActivityGenericResource,
                     self).alter_detail_data_to_serialize(request,
                                                          data)

    def obj_delete(self, bundle, **kwargs):

        r = re.search('/(\w+)/(\d+)', bundle.request.path)
        if r:
            entity_class = string.capwords(r.group(1), '_').replace('_', '')
            entity_id = r.group(2)
            obj = eval(entity_class).objects.get(id=int(entity_id))
            Activity.objects.set_activity('delete', obj)

        return super(ActivityGenericResource,
                     self).obj_delete(bundle, **kwargs)


class GenericMeta:
    list_allowed_methods = ['get', 'post']
    detail_allowed_methods = ['get', 'post', 'put', 'delete']
    authorization = DjangoAuthorization()
    authentication = SessionAuthentication()
    always_return_data = True
    include_resource_uri = False
