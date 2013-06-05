# -*- coding: utf-8 -*-
import os
import json
import logging

from django.shortcuts import (render_to_response, redirect,
                              get_object_or_404)
from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group
from django.conf import settings

from wevolve.libs.utils import generate_hash, generate_filename, upload_file
from wevolve.home.forms import RegisterForm
from wevolve.users.models import Profile
from wevolve.projects.models import ProjectPart, Project, UserProject
from wevolve.project_parts.models import File
from wevolve.activities.models import Activity
from wevolve.libs.validation import WALL_VAL
from wevolve.libs.drive_auth import get_authorization_url, get_credentials, GetCredentialsException
from wevolve.libs.drive_service import DriveUtil, connect_project_to_drive


class IndexView(TemplateView):
    def get(self, request):
        return render_to_response('index.html',
                                  context_instance=RequestContext(request))


class RegisterView(TemplateView):
    def post(self, request):
        data = json.loads(request.raw_post_data)
        data['username'] = generate_hash()[:29]
        response_data = {}
        f = RegisterForm(data)

        if not f.is_valid():
            context = RequestContext(request, {})
            context['form'] = f
            errors = dict([(k, f.error_class.as_text(v)) for k, v in f.errors.items()])
            response_data['status'] = 'failed'
            response_data['errors'] = errors

        else:
            group = Group.objects.get(name='client')
            f.save(request=request, group=group)
            response_data['status'] = 'success'

        return HttpResponse(json.dumps(response_data),
                            mimetype='application/json')


class VerifyUserRoute(TemplateView):
    def get(self, request, token):
        profile = get_object_or_404(Profile, token=token)

        if profile:
            profile.token = None
            profile.save()
            profile.user.is_active = True
            profile.user.save()
            messages.info(request, _('Welcome! Thanks for verifying your account.'))

            return redirect('/starting')


class DriveAuthView(TemplateView):
    def get(self, request):
        project = request.GET.get('project_part')
        request.session['drive_project_part'] = project
        if request.user.is_authenticated():
            return redirect(get_authorization_url(request.user.email, 1))
        else:
            response_data = {'status': 'error', 'msg': 'The user is not logged in'}
            return HttpResponse(json.dumps(response_data),
                                mimetype='application/json')

    def post(self, request):
        '''
            Connect a user to a project with Drive
        '''
        project_part = get_object_or_404(ProjectPart,
                                         pk=request.GET.get('project_part'))
        userproject = request.user.userproject_set.get(project=project_part.project)
        connect_project_to_drive(request, project_part,
                                 userproject, request.user.profile.drive_token)
        response_data = {'status': 'ok', 'msg': 'ok'}

        return HttpResponse(json.dumps(response_data),
                            mimetype='application/json')


class DriveCallback(TemplateView):
    def get(self, request):
        error = request.GET.get('error', '')
        if not error:
            credentials = get_credentials(request.GET.get('code'),
                                          1,
                                          request.user.profile)
            request.user.profile.drive_token = credentials.to_json()
            drive_util = DriveUtil(request.user.profile.drive_token)
            if not request.user.profile.drive_folder:
                folder = drive_util.insert_folder('Wevolver')
                request.user.profile.drive_folder = folder.get('id')

            request.user.profile.save()
        else:
            request.session['drive_project_part'] = None
            request.GET.get('error_description', '')
            return redirect('/#/profile?error=invalid_user')
        return redirect('/#/profile')


class DriveListView(TemplateView):
    def get(self, request):
        project_part = get_object_or_404(ProjectPart,
                                         pk=request.GET.get('project_part'))
        files = []
        project_part_folder = project_part.drive_id or None

        if request.user.is_authenticated():
            try:
                userproject = request.user.userproject_set.get(project=project_part.project)
            except UserProject.DoesNotExist:
                userproject = None

            if not userproject:
                drive_token = project_part.created_user.profile.drive_token
            elif request.user.profile.drive_token and userproject.drive_auth:
                drive_token = request.user.profile.drive_token
            elif project_part.drive_id and not request.session.get('drive_project_part', None):
                drive_token = project_part.created_user.profile.drive_token
            elif request.session.get('drive_project_part', None):
                drive_token = request.user.profile.drive_token
                connect_project_to_drive(request, project_part, userproject, drive_token)
                request.session['drive_project_part'] = None
            else:
                response_data = {'status': 'error'}
                return HttpResponse(json.dumps(response_data),
                                    mimetype='application/json')
        else:
            drive_token = project_part.created_user.profile.drive_token

        try:
            drive_util = DriveUtil(drive_token)
        except GetCredentialsException:
            logging.error('Credentials exception for %s in part %s' % (drive_token, project_part.id))
            response_data = {'status': 'error', 'msg': 'Error with drive credentials, contact with the administrator of this project'}
            return HttpResponse(json.dumps(response_data),
                                mimetype='application/json')

        if project_part_folder:
            files = drive_util.get_files("'%s' in parents" % project_part_folder)

        return HttpResponse(json.dumps(files),
                            mimetype='application/json')

    def post(self, request):
        data = json.loads(request.raw_post_data)
        file_type = data['filetype']
        project_part = get_object_or_404(ProjectPart,
                                         pk=data['project_part'])

        drive_util = DriveUtil(request.user.profile.drive_token)
        if not project_part.drive_id:
            project_part_folder = drive_util.get_project_part_folder(request.user.profile.drive_folder,
                                                                     project_part)
        else:
            project_part_folder = project_part.drive_id
        drive_file = drive_util.insert_drive_file('Untitled',
                                                  file_type, parent_id=project_part_folder)
        return HttpResponse(json.dumps(drive_file),
                            mimetype='application/json')


class DriveDetailView(TemplateView):
    def get(self, request, id):
        drive_util = DriveUtil(request.user.profile.drive_token)
        drive_util.get_file(id)

        return HttpResponse(json.dumps({'status': 'ok'}),
                            mimetype='application/json')

    def delete(self, request, id):
        drive_util = DriveUtil(request.user.profile.drive_token)
        drive_util.delete_file(id)
        return HttpResponse(json.dumps({'status': 'ok'}),
                            mimetype='application/json')


class FileUploadView(TemplateView):
    def post(self, request):
        file_uploaded = request.FILES['file']
        project_part_id = request.POST['project_part']

        if not WALL_VAL.match(file_uploaded.name):
            response_data = {'status': 'ko',
                             'message': 'The name of the file is not correct'}
        elif file_uploaded.content_type not in settings.SUPPORTED_FILES:
            response_data = {'status': 'ko',
                             'message': 'You cannot upload this kind of file'}
        elif file_uploaded.size*1.0/1048576 > settings.FILE_SIZE:
            response_data = {'status': 'ko',
                             'message': 'You cannot upload a file bigger than %d MB' % settings.FILE_SIZE}
        else:
            project_part = ProjectPart.objects.get(pk=project_part_id)
            file_obj = File(created_user=request.user,
                            original_name=file_uploaded.name,
                            system_name=file_uploaded.name,
                            project_part=project_part)
            if os.path.exists(file_obj.get_file_path(True)):
                file_obj.set_original_name()
            with open(file_obj.get_file_path(True), 'wb+') as destination:
                for chunk in file_uploaded.chunks():
                    destination.write(chunk)

            if(file_obj.is_image()):
                file_obj.generate_thumbnail()
            file_obj.save()
            Activity.objects.set_activity('add', file_obj)

            if request.user.profile.drive_token and project_part.project.drive_id:
                drive_util = DriveUtil(request.user.profile.drive_token)
                if not project_part.drive_id:
                    project_part_folder = drive_util.get_project_part_folder(request.user.profile.drive_folder,
                                                                             project_part)
                else:
                    project_part_folder = project_part.drive_id
                drive_util.insert_file(file_uploaded.name,
                                       'description', project_part_folder,
                                       file_uploaded.content_type,
                                       file_obj.get_file_path(True))

            response_data = {'status': 'ok'}
        return HttpResponse(json.dumps(response_data),
                            mimetype='application/json')


class ImageUpload(TemplateView):
    def post(self, request, type_upload):
        response_data = {'status': 'ko',
                         'message': 'Error in parameters'}
        file_uploaded = request.FILES['file']

        if not WALL_VAL.match(file_uploaded.name):
            response_data = {'status': 'ko',
                             'message': 'The name of the file is not correct'}
        elif file_uploaded.content_type not in settings.SUPPORTED_FILES:
            response_data = {'status': 'ko',
                             'message': 'You cannot upload this kind of file'}
        elif file_uploaded.size*1.0/1048576 > settings.FILE_SIZE:
            response_data = {'status': 'ko',
                             'message': 'You cannot upload a file bigger than %d MB' % settings.FILE_SIZE}
        elif type_upload == 'profile':
            entity = request.POST['entity']
            project_id = None
            if 'project' in request.POST:
                project_id = request.POST['project']

            if entity in ('project', 'user'):
                new_filename = generate_filename(file_uploaded.name)

                if entity == 'project':
                    obj = get_object_or_404(Project, id=project_id)
                    obj.image_name = new_filename
                    obj.save()
                elif entity == 'user':
                    request.user.profile.picture_name = new_filename
                    request.user.profile.save()

                upload_file(file_uploaded, entity, new_filename)
                response_data = {'status': 'ok',
                                 'message': 'File uploaded correctly'}
        elif type_upload == 'document':
            relative_path = upload_file(file_uploaded, 'documents', with_subpath=True)
            response_data = {'status': 'ok',
                             'message': 'File uploaded correctly',
                             'url': relative_path}

        return HttpResponse(json.dumps(response_data),
                            mimetype='application/json')


class PasswordResetDoneView(TemplateView):
    def get(self, request):
        messages.info(request, _('An e-mail has been '
                                 'send to you which explains how to reset your password'))
        return redirect('/')


class PasswordResetCompleteView(TemplateView):
    def get(self, request):
        pass
        #return redirect('/')
