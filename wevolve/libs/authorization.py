import re
import json

from tastypie.authorization import Authorization


class GenericAuthorization(Authorization):
    def create_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no create list.")

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no update list.")
