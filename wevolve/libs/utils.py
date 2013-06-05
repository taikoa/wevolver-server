# -*- coding: utf-8 -*-
import os
from lxml import html
import hashlib
import uuid

from django.core.urlresolvers import reverse
from django.conf import settings


def parse_html(url, content):
    """Parse HTML for the Wall"""
    html_element = html.document_fromstring(content)
    title = html_element.find('head/title').text
    description = ''

    images = html_element.xpath('//img')
    metas = html_element.xpath('//meta')

    for meta in metas:
        if meta.get('name') == 'description' or meta.get('property') == 'og:description':
            description = meta.get('content')
            break

    first_image = None

    if images:
        first_image = images[0].get('src')

    result = {}
    result['image'] = first_image
    result['title'] = title
    result['description'] = description

    return result


def generate_hash():
    return hashlib.md5(str(uuid.uuid1())).hexdigest()


def verify_user_route(request, token):
    return request.build_absolute_uri(reverse('verify_user', args=(token,)))


def get_extension(filename):
    try:
        return filename.split('.')[-1]
    except IndexError:
        return ''


def generate_filename(filename):
    return '.'.join([generate_hash(), get_extension(filename)])


def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def upload_file(file_obj, path, filename=None, with_subpath=False):
    if not filename:
        new_filename = generate_filename(file_obj.name)
    else:
        new_filename = filename
    relative_path = path

    if with_subpath:
        subpath = new_filename[0:2]
        relative_path = os.path.join(relative_path, subpath)
        create_path(os.path.join(settings.MEDIA_ROOT,
                    relative_path))

    relative_path = os.path.join(relative_path,
                                 '%s' % new_filename)
    with open(os.path.join(settings.MEDIA_ROOT,
                           relative_path), 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    return os.path.join(settings.MEDIA_URL,
                        relative_path)
