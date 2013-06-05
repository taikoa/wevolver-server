from tastypie.validation import Validation

from wevolve.projects.models import Project
from wevolve.libs.validation import WORD_VAL, WALL_VAL


class ProjectValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        if 'title' in bundle.data and request.method == 'POST':
            try:
                project = Project.objects.get(title=bundle.data['title'])
            except Project.DoesNotExist:
                project = None
            if project:
                errors['title'] = 'There is another project with this title'

        if 'title' in bundle.data and request.method in ('POST', 'PUT'):
            if not WALL_VAL.match(bundle.data['description']):
                errors['description'] = 'The description is not correct'
            if 'tags' in bundle.data:
                if not WALL_VAL.match(bundle.data['tags']):
                    errors['tags'] = 'The tags are not correct'

        return errors


class ProjectPartValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        if 'title' in bundle.data:
            if not WORD_VAL.match(bundle.data['title']):
                errors['title'] = 'The title is not correct'

        return errors
