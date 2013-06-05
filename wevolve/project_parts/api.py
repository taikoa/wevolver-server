import os

from tastypie.resources import ALL
from tastypie import fields
from tastypie.utils import now
from tastypie.authorization import Authorization
from tastypie.authentication import (Authentication, MultiAuthentication,
                                     SessionAuthentication)

from wevolve.libs.serializers import DatetimeSerializer
from wevolve.project_parts.authorization import (ProjectPartElemAuthorization,
                                        CommentAuthorization)
from wevolve.project_parts.models import Document, File, Post, Comment
from wevolve.project_parts.validation import (PostValidation, CommentValidation, DocumentValidation)
from wevolve.projects.api import ProjectPartResource
from wevolve.tasks.api import TaskResource
from wevolve.libs.generic_resource import (GenericResource, GenericMeta,
                                           ActivityGenericResource)
from wevolve.activities.models import Activity
from wevolve.libs.oauthauthentication import OAuth20Authentication


class DocumentResource(GenericResource):
    project_part = fields.ForeignKey(ProjectPartResource, 'project_part')
    #comments = fields.ToManyField('wevolve.project_parts.api.CommentResource',
                                  #'comment_set',
                                  #full=True,
                                  #null=True)

    class Meta(GenericMeta):
        queryset = Document.objects.all()
        resource_name = 'document'
        authorization = ProjectPartElemAuthorization()
        authentication = MultiAuthentication(OAuth20Authentication(),
                                             SessionAuthentication(), Authentication())
        filtering = {'project_part': ALL}

    def obj_create(self, bundle, **kwargs):
        created = now()
        return super(DocumentResource, self).obj_create(bundle,
                                                        created=created,
                                                        status=0,
                                                        created_user=bundle.request.user)

    def obj_update(self, bundle, **kwargs):
        bundle_cleaned = DocumentValidation().clean_data(bundle)
        return super(DocumentResource, self).obj_update(bundle_cleaned,
                                                        **kwargs)

class FileResource(GenericResource):
    project_part = fields.ForeignKey(ProjectPartResource, 'project_part')
    created = fields.DateTimeField(attribute='created', readonly=True)
    username = fields.CharField(readonly=True)
    avatar = fields.CharField(readonly=True)
    image_file = fields.CharField(readonly=True)
    url = fields.CharField(readonly=True)

    class Meta(GenericMeta):
        queryset = File.objects.all()
        resource_name = 'file'
        filtering = {'project_part': ALL}
        authorization = ProjectPartElemAuthorization()
        authentication = MultiAuthentication(OAuth20Authentication(),
                                             SessionAuthentication(),
                                             Authentication())
        serializer = DatetimeSerializer()
        ordering = ['-original_name']
        allowed_methods = ['GET', 'DELETE']

    def dehydrate_username(self, bundle):
        return " ".join([bundle.obj.created_user.first_name,
                         bundle.obj.created_user.last_name])

    def dehydrate_avatar(self, bundle):
        return bundle.obj.created_user.profile.get_image_profile()

    def dehydrate_image_file(self, bundle):
        if bundle.obj.thumbnail:
            return os.path.join('/media/files/',
                                str(bundle.obj.project_part.id),
                                'thumbnails',
                                bundle.obj.thumbnail)
        else:
            extension = bundle.obj.original_name.split('.')[1].lower()
            return os.path.join('/static/images/file_extensions/',
                                '%s.png' % extension)

    def dehydrate_url(self, bundle):
        return os.path.join('/media/files/',
                            str(bundle.obj.project_part.id),
                            bundle.obj.original_name)

    def obj_delete(self, **kwargs):
        file_obj = File.objects.get(pk=kwargs['pk'])
        file_obj.delete_file()
        Activity.objects.set_activity('delete', file_obj)

        return super(FileResource, self).obj_delete(**kwargs)


class PostResource(ActivityGenericResource):
    project_part = fields.ForeignKey(ProjectPartResource, 'project_part')
    image_name = fields.CharField(attribute='image_name', null=True,
                                  readonly=True)
    image_original_name = fields.CharField(attribute='image_original_name',
                                           null=True, readonly=True)
    username = fields.CharField(readonly=True)
    avatar = fields.CharField(readonly=True)
    created = fields.DateTimeField(attribute='created', readonly=True)

    # Relations
    comments = fields.ToManyField('wevolve.project_parts.api.CommentResource',
                                  'comment_set',
                                  full=True,
                                  null=True,
                                  readonly=True)

    class Meta(GenericMeta):
        queryset = Post.objects.all()
        resource_name = 'post'
        filtering = {'project_part': ALL}
        authorization = ProjectPartElemAuthorization()
        authentication = MultiAuthentication(OAuth20Authentication(),
                                             SessionAuthentication(),
                                             Authentication())
        #ordering = ['created']
        serializer = DatetimeSerializer()
        validation = PostValidation()

    def obj_create(self, bundle, **kwargs):
        created = now()
        result = super(PostResource, self).obj_create(bundle,
                                                      created=created,
                                                      created_user=bundle.request.user)
        bundle.obj.set_post_data()
        return result

    def dehydrate_username(self, bundle):
        return " ".join([bundle.obj.created_user.first_name,
                         bundle.obj.created_user.last_name])

    def dehydrate_avatar(self, bundle):
        return bundle.obj.created_user.profile.get_image_profile()


class CommentResource(ActivityGenericResource):
    task = fields.ForeignKey(TaskResource, 'task', null=True)
    post = fields.ForeignKey(PostResource, 'post', null=True)
    username = fields.CharField(readonly=True)
    avatar = fields.CharField(readonly=True)
    created = fields.DateTimeField(attribute='created', readonly=True)

    # Relations
    project_part = fields.ForeignKey(ProjectPartResource, 'project_part',
                                     null=True)

    class Meta(GenericMeta):
        queryset = Comment.objects.all()
        resource_name = 'comment'
        filtering = {'project_part': ALL,
                     'task': ALL,
                     'post': ALL
                     }
        serializer = DatetimeSerializer()
        authorization = CommentAuthorization()
        validation = CommentValidation()

    def obj_create(self, bundle, **kwargs):
        created = now()
        return super(CommentResource, self).obj_create(bundle,
                                                       created=created,
                                                       created_user=bundle.request.user)

    def dehydrate_username(self, bundle):
        return " ".join([bundle.obj.created_user.first_name,
                         bundle.obj.created_user.last_name])

    def dehydrate_avatar(self, bundle):
        return bundle.obj.created_user.profile.get_image_profile()
