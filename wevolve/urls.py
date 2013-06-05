from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from tastypie.api import Api
from email_login import adminsite
from email_login.forms import EmailAuthenticationForm

from wevolve import settings
from wevolve.home.views import (PasswordResetDoneView,
                                PasswordResetCompleteView,
                                RegisterView,
                                IndexView,
                                VerifyUserRoute,
                                FileUploadView,
                                ImageUpload,
                                DriveAuthView,
                                DriveCallback,
                                DriveListView,
                                DriveDetailView)
from wevolve.projects.api import ProjectResource, ProjectPartResource
from wevolve.project_parts.api import DocumentResource, FileResource, PostResource, CommentResource
from wevolve.tasks.api import TaskResource
from wevolve.users.api import UserResource, ProfileResource
from wevolve.home.api import CategoryResource
from wevolve.activities.api import ActivityResource


admin.autodiscover()
site = adminsite.EmailLoginAdminSite()
# duplicate the normal admin's registry until ticket #8500 get's fixed
site._registry = admin.site._registry

# Tastypie
v1_api = Api(api_name='v1')

# Projects
v1_api.register(ProjectResource())
v1_api.register(ProjectPartResource())

# Project Parts
v1_api.register(DocumentResource())
v1_api.register(FileResource())
v1_api.register(PostResource())
v1_api.register(CommentResource())

# Tasks
v1_api.register(TaskResource())

# Users
v1_api.register(UserResource())
v1_api.register(ProfileResource())

# Home
v1_api.register(CategoryResource())

#Activities
v1_api.register(ActivityResource())

urlpatterns = patterns('',
    # url(r'^profiler/', include('profiler.urls')),
    url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),
    (r'^robots\.txt$', direct_to_template,
     {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    (r'api/', include(v1_api.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html',
         'authentication_form': EmailAuthenticationForm}, name='auth_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'},
        name="logout"),
    url(r'^register/', RegisterView.as_view(), name='register_view'),
    url(r'^drive_auth/', DriveAuthView.as_view(), name='drive_auth'),
    url(r'^oauth2callback/', DriveCallback.as_view(), name='drive_callback'),
    url(r'^drive/(?P<id>[\w\-]+)', DriveDetailView.as_view(), name='drive_detail'),
    url(r'^drive/', DriveListView.as_view(), name='drive_list'),
    url(r'^upload_file/', FileUploadView.as_view(), name='upload_file'),
    url(r'^upload_image/(?P<type_upload>\w+)', ImageUpload.as_view(),
        name='upload_profile'),
    url(r'user/verify/(?P<token>\w+)', VerifyUserRoute.as_view(),
        name='verify_user'),
    (r'^account/', include('email_login.urls')),

    # Reset password
    # url(r'^password/reset/$',
    #     auth_views.password_reset,
    #     {'template_name': 'accounts/password_reset.html',
    #     'email_template_name': 'accounts/emails/password_reset_message.txt',
    #     'post_reset_redirect': reverse_lazy('password_reset_done'),
    #     'extra_context': {'title': _('Reset password')},
    #      },
    #     name='password_reset'),

    # url(r'^password/reset/done/$',
    #     PasswordResetDoneView.as_view(),
    #     name='password_reset_done'),

    # url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #     auth_views.password_reset_confirm,
    #     {'template_name': 'accounts/password_reset_confirm_form.html',
    #     'post_reset_redirect': reverse_lazy('password_reset_complete'),
    #     'extra_context': {'title': _('Reset password')},
    #      },
    #     name='password_reset_confirm'),

    # url(r'^password/reset/confirm/complete/$',
    #     PasswordResetCompleteView.as_view(),
    #     name='password_reset_complete'),

    # # Change password
    # url(r'password/change/$',
    #     auth_views.password_change,
    #     {'template_name': 'accounts/password_reset.html',
    #      'post_change_redirect': reverse_lazy('edit_profile'),
    #      'extra_context': {'title': _('Change password')},
    #      },
    #     name='password_change'),
    url(r'^admin/', include(site.urls)),
    url('^$', IndexView.as_view(), name="home-index")
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^starting/$', 'flatpage', {'url': '/starting/'}, name='starting'),
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
    url(r'^learn/$', 'flatpage', {'url': '/learn/'}, name='learn')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
