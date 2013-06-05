from tastypie.validation import Validation

from wevolve.libs.validation import TASK_VAL, WALL_VAL


class TaskValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        if 'description' in bundle.data:
            if not WALL_VAL.match(bundle.data['description']):
                errors['description'] = 'The description is not correct'

        return errors
