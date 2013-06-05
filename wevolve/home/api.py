from tastypie.authorization import ReadOnlyAuthorization
from tastypie.authentication import Authentication

from wevolve.home.models import Category
from wevolve.libs.generic_resource import GenericResource, GenericMeta


class CategoryResource(GenericResource):
    class Meta(GenericMeta):
        queryset = Category.objects.all()
        resource_name = 'category'
        #authorization = ReadOnlyAuthorization()
        #authentication = Authentication()
        #allowed_methods = ['GET']
