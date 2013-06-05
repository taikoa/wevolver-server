from tastypie.validation import Validation

from wevolve.libs.validation import WORD_VAL, WALL_VAL


class ProfileValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        if 'state' in bundle.data:
            if bundle.data['state'] and not WORD_VAL.match(bundle.data['state']):
                errors['state'] = 'The state is not correct'
        if 'city' in bundle.data:
            if bundle.data['city'] and not WORD_VAL.match(bundle.data['city']):
                errors['city'] = 'The city is not correct'
        if 'twitter' in bundle.data:
            if bundle.data['twitter'] and not WORD_VAL.match(bundle.data['twitter']):
                errors['twitter'] = 'twitter account is not correct'
        if 'facebook' in bundle.data:
            if bundle.data['facebook'] and not WALL_VAL.match(bundle.data['facebook']):
                errors['facebook'] = 'The facebook is not correct'
        if 'linkedin' in bundle.data:
            if bundle.data['linkedin'] and not WALL_VAL.match(bundle.data['linkedin']):
                errors['linkedin'] = 'The linkedin is not correct'
        return errors
