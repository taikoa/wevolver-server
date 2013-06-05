import re
import json
import logging

from tastypie.exceptions import Unauthorized

from wevolve.libs.authorization import GenericAuthorization
from wevolve.projects.models import ProjectPart, UserProject
from wevolve.project_parts.models import Comment, Post
from wevolve.tasks.models import Task


class ProjectPartElemAuthorization(GenericAuthorization):
    def get_project(self, bundle):
        project_part = bundle.request.GET.get('project_part', None)
        if bundle.request.method == 'POST':
            data = json.loads(bundle.request.raw_post_data)
        else:
            data = None
        if not project_part:
            try:
                if 'pk' in data['project_part']:
                    project_part = data['project_part']['pk']
                elif 'id' in data['project_part']:
                    project_part = data['project_part']['id']
            except KeyError:
                logging.error('No key project_part')
                pass
            except TypeError:
                # Its an url
                r = re.search('/project_part/(\d+)', bundle.request.path)
                if r:
                    project_part = r.group(1)
            try:
                project_part = bundle.obj.project_part.id
            except ProjectPart.DoesNotExist:
                pass

        if not project_part:
            return False
        else:
            try:
                project_part_obj = ProjectPart.objects.get(pk=int(project_part))
            except ProjectPart.DoesNotExist:
                return False
            return project_part_obj.project

    def check_user_and_permission(self, bundle):
        if not bundle.request.user.is_authenticated():
            return False
        project = self.get_project(bundle)
        if not project:
            return False
        else:
            if project.is_open():
                return True
            user_project = bundle.request.user.userproject_set.filter(project=project)
            if not user_project:
                return False
        return True

    def check_is_open(self, bundle):
        project = self.get_project(bundle)
        if not project:
            return False
        else:
            return project.is_open()

    def check_all_perms(self, bundle):
        if not bundle.request.user.is_authenticated():
            return self.check_is_open(bundle)
        else:
            return self.check_user_and_permission(bundle)
        raise Unauthorized('You don\'t have access')

    def read_list(self, object_list, bundle):
        user_id = int(bundle.request.GET.get('user', 0))
        if bundle.request.user.is_authenticated() and bundle.request.user.id == user_id:
            return object_list
        elif self.check_all_perms(bundle):
            return object_list
        else:
            raise Unauthorized('You don\'t have access')

    def read_detail(self, object_list, bundle):
        return self.check_all_perms(bundle)

    def create_detail(self, object_list, bundle):
        if not self.check_user_and_permission(bundle):
            raise Unauthorized("Sorry, no access")
        else:
            return True

    def update_detail(self, object_list, bundle):
        if not self.check_user_and_permission(bundle):
            raise Unauthorized("Sorry, no access")
        else:
            return True

    def delete_detail(self, object_list, bundle):
        if not bundle.request.user.is_authenticated():
            raise Unauthorized('You cannot delete it')
        else:
            project = bundle.obj.project_part.project
            try:
                bundle.request.user.userproject_set.get(project=project)
            except UserProject.DoesNotExist:
                raise Unauthorized('You cannot delete it')
        return self.check_user_and_permission(bundle)


class CommentAuthorization(GenericAuthorization):
    def check_user_and_permission(self, bundle):
        project_part = None

        if bundle.request.method == 'GET':
            # FIXME Check if user is in the project
            return True

        elif bundle.request.method in ('PUT', 'DELETE'):
            # Get project part
            r = re.search('/comment/(\d+)', bundle.request.path)
            if r:
                comment_obj = Comment.objects.get(pk=r.group(1))
                if comment_obj:
                    if comment_obj.task:
                        project_part = comment_obj.task.project_part
                    elif comment_obj.post:
                        project_part = comment_obj.post.project_part
            else:
                raise Unauthorized('You cannot access')

        elif bundle.request.method == 'POST':
            data = json.loads(bundle.request.raw_post_data)
            if 'post' in data and data['post']:
                project_part = Post.objects.get(pk=data['post']['pk']).project_part
            elif 'task' in data and data['task']:
                project_part = Task.objects.get(pk=data['task']['pk']).project_part

        if not project_part:
            raise Unauthorized('You cannot access')
        else:
            user_project = bundle.request.user.userproject_set.filter(project=int(project_part.project.id))

        if not user_project:
            raise Unauthorized('You cannot access')
        return True

    def read_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)

    def create_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)

    def update_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)

    def delete_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)
