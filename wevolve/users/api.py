import json

from django.contrib.auth.models import User
from django.db.models import Q
from django.conf.urls.defaults import url
from django.http import HttpResponse
from django.forms.models import model_to_dict
from tastypie import fields
from tastypie.utils import trailing_slash
from tastypie.authentication import (Authentication, MultiAuthentication,
                                     SessionAuthentication)

from wevolve.users.models import Skill, UserSkill, Profile
from wevolve.libs.generic_resource import GenericResource, GenericMeta
from wevolve.users.authorization import UserAuthorization
from wevolve.users.validation import ProfileValidation
from wevolve.libs.oauthauthentication import OAuth20Authentication


class ProfileResource(GenericResource):
    country = fields.CharField(attribute='country')
    city = fields.CharField(attribute='city')
    picture_name = fields.CharField(readonly=True, blank=True, null=True)
    picture_original_name = fields.CharField(readonly=True, blank=True,
                                             null=True)
    interests = fields.CharField(readonly=True, blank=True, null=True)
    skills = fields.CharField(readonly=True, blank=True, null=True)
    bio = fields.CharField('bio', blank=True, null=True)
    status = fields.IntegerField(readonly=True, null=True, default=0)
    token = fields.CharField(readonly=True, blank=True, null=True)
    modified = fields.DateTimeField(readonly=True, null=True, blank=True)
    twitter = fields.CharField('twitter', blank=True, null=True)
    facebook = fields.CharField('facebook', blank=True, null=True)
    linkedin = fields.CharField('linkedin', blank=True, null=True)
    has_drive = fields.BooleanField()

    class Meta(GenericMeta):
        queryset = Profile.objects.all()
        resource_name = 'profile'
        authorization = UserAuthorization()
        authentication = MultiAuthentication(OAuth20Authentication(),
                                             SessionAuthentication(),
                                             Authentication())
        validation = ProfileValidation()
        fields = ['id', 'user', 'country', 'city', 'state',
                  'picture_name', 'picture_original_name',
                  'bio', 'modified', 'username',
                  'twitter', 'facebook', 'linkedin']

    def obj_create(self, bundle, **kwargs):
        return super(GenericResource, self).obj_create(bundle,
                                                       user=bundle.request.user)

    def dehydrate_picture_name(self, bundle):
        return bundle.obj.get_image_profile()

    def dehydrate_has_drive(self, bundle):
        return bool(bundle.obj.drive_folder)


class UserResource(GenericResource):
    username = fields.CharField(readonly=True)
    first_name = fields.CharField(readonly=True)
    last_name = fields.CharField(readonly=True)
    image_profile = fields.CharField(readonly=True)
    # Relations
    projects = fields.ListField()
    profile = fields.ForeignKey(ProfileResource, 'profile',
                                null=True, full=True)
    # Other fields
    number_projects = fields.IntegerField(readonly=True)

    class Meta(GenericMeta):
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = UserAuthorization()
        authentication = MultiAuthentication(SessionAuthentication(), Authentication())
        fields = ['first_name', 'email', 'last_name', 'date_joined',
                  'image_profile', 'id', 'number_projects', 'profile',
                  'projects', 'username']

    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/settings%s$"
                    % (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('user_settings'), name="api_user_settings"),
                url(r"^(?P<resource_name>%s)/find%s$"
                    % (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('user_find'), name="api_user_find")
                ]

    def user_settings(self, request, **kwargs):
        '''
            Get the properties of the user currently authenticated
        '''

        if request.user.is_authenticated():
            if request.method == 'GET':
                user = User.objects.get(email=request.user.email)
                bundle = self.build_bundle(obj=user, request=request)
                bundle = self.full_dehydrate(bundle)

                return self.create_response(request, bundle)
            elif request.method == 'PUT':
                return self.put_detail(request)
        else:
            response_data = {'status': 'ko'}
            return HttpResponse(json.dumps(response_data),
                                mimetype='application/json')

    def user_find(self, request, **kwargs):
        '''
            Get the properties of the user currently authenticated
        '''
        if request.user.is_authenticated():
            if request.method == 'GET':
                query = request.GET.get('user', None)
                if not query:
                    response = HttpResponse('Unauthorized')
                    response.status_code = 401
                    return response
                else:
                    users = User.objects.filter(Q(first_name__icontains=query) |
                                                Q(last_name__icontains=query))
                    bundles = []
                    user_dict = {}
                    for user in users:
                        user_dict = model_to_dict(user)
                        user_dict = {'username': ' '.join([user_dict['first_name'],
                                                          user_dict['last_name']]),
                                     'id': user.id,
                                     'image_profile': user.profile.get_image_profile()
                                     }
                        bundles.append(self.build_bundle(data=user_dict,
                                                         request=request))

                    return self.create_response(request,
                                                bundles)

    def dehydrate_projects(self, bundle):
        userprojects = [userproject for userproject in bundle.obj.userproject_set.all()]
        bundles = []
        for userproject in userprojects:
            # Secret projects
            if bundle.request.user != bundle.obj and userproject.project.type_field == 2:
                continue

            project = userproject.project
            project_aux = model_to_dict(project)
            project_aux = {'id': project.id, 'title': project.title,
                           'description': project.description,
                           'auth': project.get_user_permission(bundle.request.user),
                           'members': project.members(bundle.obj)}
            bundles.append(self.build_bundle(data=project_aux, request=bundle.request))
        return bundles

    def dehydrate_username(self, bundle):
        return " ".join([bundle.obj.first_name, bundle.obj.last_name])

    def dehydrate_image_profile(self, bundle):
        return bundle.obj.profile.get_image_profile()

    def dehydrate_number_projects(self, bundle):
        return bundle.obj.userproject_set.count()

    def build_filters(self, filters=None):
        # TODO remove the current user from filter
        if filters is None:
            filters = {}

        orm_filters = super(UserResource, self).build_filters(filters)

        if "find" in filters:
            query = filters['find']
            users = User.objects.filter(Q(first_name__icontains=query) |
                                        Q(last_name__icontains=query))
            orm_filters['pk__in'] = [u.pk for u in users]

        return orm_filters


class SkillResource(GenericResource):
    class Meta(GenericMeta):
        queryset = Skill.objects.all()
        resource_name = 'skill'
        allowed_methods = ['GET']


class UserSkillResource(GenericResource):
    class Meta(GenericMeta):
        queryset = UserSkill.objects.all()
        resource_name = 'user_skill'
        allowed_methods = ['GET']
