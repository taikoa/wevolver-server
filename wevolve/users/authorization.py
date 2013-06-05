import re

from tastypie.exceptions import Unauthorized

from wevolve.libs.authorization import GenericAuthorization


class UserAuthorization(GenericAuthorization):
    def check_user_and_permission(self, bundle):
        # For the project network
        if not bundle.request.user.is_authenticated() and \
           bundle.request.method == 'GET' \
           and bundle.request.GET.get('with_members'):
            return True

        elif bundle.request.method != 'GET' and bundle.request.user.is_authenticated():
            ruser = re.search('/user/(\d+)', bundle.request.path)
            rprofile = re.search('/profile/(\d+)', bundle.request.path)

            # FIXME Workaround to fix Tastypie strange behaviour
            rother = re.search('/(user|profile)/', bundle.request.path)
            if not rother:
                return True

            if ruser or rprofile:
                if ruser:
                    user_id = ruser.group(1)
                elif rprofile:
                    user_id = rprofile.group(1)

                if not int(user_id) == bundle.request.user.profile.id:
                    raise Unauthorized("Sorry, no deletes.")
            else:
                raise Unauthorized("Sorry, no User Auth.")
        return True

    def read_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)

    def create_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)

    def update_detail(self, object_list, bundle):
        return self.check_user_and_permission(bundle)

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")
