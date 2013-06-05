import re

import bleach
from tastypie.validation import Validation
from django.conf import settings

from wevolve.libs.validation import WORD_VAL, WALL_VAL


def check_domains(attr_name, attr_value):
    if attr_name == 'src':
        for domain in settings.SUPPORTED_VIDEO_DOMAINS:
            if re.match('^https?://%s' % domain, attr_value):
                return True
        return False
    return True

def check_images(attr_name, attr_value):
    return True


class PostValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'There is no data'}

        errors = {}

        if 'content' in bundle.data:
            if not WALL_VAL.match(bundle.data['content']):
                errors['content'] = ['The content is not correct']

        return errors


class CommentValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'There is no data'}

        errors = {}

        if 'text' in bundle.data:
            if not WALL_VAL.match(bundle.data['text']):
                errors['text'] = ['The text is not correct']

        return errors


class DocumentValidation(Validation):
    def clean_data(self, bundle):
        errors = {}
        errors['text'] = ['The text is not correct']
        bleach.ALLOWED_TAGS += ['iframe', 'img', 'u', 'h1',
                                'h2', 'h3', 'h4', 'h5', 'h6',
                                'blockquote', 'br', 'span', 'p',
                                'div']
        bleach.ALLOWED_ATTRIBUTES['iframe'] = check_domains
        bleach.ALLOWED_ATTRIBUTES['img'] = check_images

        try:
            bundle.data['text'] = bleach.clean(bundle.data['text'])
        except KeyError:
            return errors
        return bundle
