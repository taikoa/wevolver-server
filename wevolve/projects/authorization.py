import re

from tastypie.exceptions import Unauthorized

from wevolve.libs.authorization import GenericAuthorization
from wevolve.projects.models import UserProject, ProjectPart


class ProjectAuthorization(GenericAuthorization):
    def check_user_and_permission(self, bundle):
        if not re.search('/project/', bundle.request.path):
            return True
        if not bundle.request.user.is_authenticated() and bundle.request.method in ('PUT', 'POST', 'DELETE'):
            return False
        try:
            user_project = bundle.request.user.userproject_set.get(project=bundle.obj)
            if bundle.request.method == 'PUT':
                return True
            if user_project.is_admin() and bundle.request.method == 'DELETE':
                return True
        except UserProject.DoesNotExist:
            pass
        raise Unauthorized('You cannot perform this action in project')

    def read_list(self, object_list, bundle):
        if bundle.request.user.is_authenticated() or bundle.request.GET.get('open', None):
            return object_list
        raise Unauthorized('You cannot create a project')

    def read_detail(self, object_list, bundle):
        if bundle.obj.is_open():
            return True
        else:
            if not bundle.request.user.is_authenticated() or \
               not len(bundle.obj.userproject_set.filter(user=bundle.request.user)):
                raise Unauthorized('You cannot access this project')
        return True

    def create_detail(self, object_list, bundle):
        if bundle.request.user.is_authenticated():
            return True
        raise Unauthorized('You cannot create a project')

    def update_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)

    def delete_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)


class ProjectPartAuthorization(GenericAuthorization):
    def check_user_and_permission(self, bundle):
        #FIXME Tastypie will enter here when using Entities related to it
        if not re.search('/project_part/', bundle.request.path):
            return True

        if not bundle.request.user.is_authenticated():
            raise Unauthorized('You don\'t have access')
        try:
            if bundle.request.method == 'POST':
                try:
                    user_project = bundle.request.user.userproject_set.filter(project=bundle.data['project_id']['pk'])
                except KeyError:
                    # FIXME When there is a project_part_id Tastypie access twice
                    # in the authorization check, the second it crash
                    if len(bundle.data.items()) == 1 and 'pk' in bundle.data:
                        return True
                    else:
                        raise Unauthorized('You dont have access, Project part')

            else:
                project_part = bundle.obj
                user_project = bundle.request.user.userproject_set.filter(project=project_part.project)
            return True
        except UserProject.DoesNotExist:
            raise Unauthorized('You dont have access, Project part')
        except KeyError:
            raise Unauthorized('You dont have access, Project part, the id is wrong')

    def read_list(self, object_list, bundle):
        raise Unauthorized('You dont have access, Project part')

    def read_detail(self, object_list, bundle):
        if bundle.obj.project.is_open():
            return True
        return self.check_user_and_permission(bundle)

    def create_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)

    def update_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)

    def delete_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)
