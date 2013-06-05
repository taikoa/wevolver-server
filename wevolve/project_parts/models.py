import os
import re
import mimetypes

from PIL import Image
from StringIO import StringIO
from requests import ConnectionError
import requests
from urlparse import urlparse
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import Http404
from tastypie.utils import now

from wevolve.projects.models import ProjectPart
from wevolve.tasks.models import Task
from wevolve.libs.utils import (generate_hash, generate_filename,
                                get_extension, parse_html)
import logging


class Document(models.Model):
    project_part = models.ForeignKey(ProjectPart)
    text = models.TextField(blank=True)
    status = models.IntegerField()
    created_user = models.ForeignKey(User,
                                     related_name='document_created_user')
    created = models.DateTimeField(default=now(),
                                   null=True, blank=True)
    modified_user = models.ForeignKey(User, null=True,
                                      blank=True,
                                      related_name='document_modified_user')
    modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'document'


class File(models.Model):
    project_part = models.ForeignKey(ProjectPart)
    original_name = models.CharField(max_length=765, null=True)
    system_name = models.CharField(max_length=765, null=True)
    properties = models.CharField(max_length=765, null=True)
    thumbnail = models.CharField(max_length=765, null=True)
    created_user = models.ForeignKey(User)
    created = models.DateTimeField(default=now(), null=True,
                                   blank=True)

    class Meta:
        db_table = u'file'

    def is_image(self):
        mimetype = mimetypes.guess_type(self.get_file_path(True))
        if mimetype[0] in settings.SUPPORTED_IMAGES:
            return True
        return False

    def get_file_path(self, with_file=False):
        file_path = os.path.join(settings.MEDIA_ROOT, 'files',
                                 '%d' % self.project_part.id)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        if with_file:
            file_path = os.path.join(file_path, self.original_name)
        return file_path

    def get_thumbnail_path(self, with_file=False):
        thumbnail_path = os.path.join(self.get_file_path(),
                                      'thumbnails')
        if not os.path.exists(thumbnail_path):
            os.makedirs(thumbnail_path)

        if with_file:
            thumbnail_path = os.path.join(thumbnail_path,
                                          self.thumbnail)
        return thumbnail_path

    def generate_thumbnail(self):
        thumbnail_path = self.get_thumbnail_path()
        thumbnail_name = generate_filename(self.original_name)
        thumbnail_path = os.path.join(thumbnail_path,
                                      thumbnail_name)
        image_file = Image.open(self.get_file_path(True))
        image_file.thumbnail(settings.THUMBS_SIZE, Image.ANTIALIAS)
        image_file.save(thumbnail_path, image_file.format)
        self.thumbnail = thumbnail_name

    def set_original_name(self):
        name_index = 1
        namefile = self.original_name
        # FIXME
        self.original_name = ''.join([namefile.split('.')[0],
                                     '(%d).' % name_index,
                                     get_extension(self.original_name)])
        while os.path.exists(self.get_file_path(True)):
            name_index += 1
            self.original_name = ''.join([namefile.split('.')[0],
                                         '(%d).' % name_index,
                                         get_extension(self.original_name)])
        self.system_name = self.original_name

    def delete_file(self):
        try:
            if self.is_image():
                os.remove(self.get_thumbnail_path(True))
            os.remove(self.get_file_path(True))
        except OSError:
            # No files
            pass


class Post(models.Model):
    project_part = models.ForeignKey(ProjectPart)
    content = models.TextField()
    image_name = models.CharField(max_length=255, null=True)
    image_original_name = models.CharField(max_length=255, null=True)
    created_user = models.ForeignKey(User, related_name='post_created_user')
    created = models.DateTimeField(default=now(),
                                   null=True, blank=True)

    class Meta:
        db_table = u'post'
        ordering = ['-created']

    def __unicode__(self):
        return u'%s' % self.content

    def get_content_url(self, url):
        try:
            response = requests.get(url, timeout=3)
        except ConnectionError:
            raise Http404

        if response.status_code == 200:
            html_content = parse_html(url, response.content)
            image_res_url = ''

            # FIXME we could leave this out
            if html_content['image']:
                if not re.search('(https?:\/\/[\w+\.]*)',
                                 html_content['image']):
                    url_parsed = urlparse(url)
                    image_url = '/'.join(['://'.join([url_parsed.scheme,
                                          url_parsed.netloc]), html_content['image']])
                else:
                    image_url = html_content['image']

                image_ext = html_content['image'].split('.')[-1].lower()

                if len(image_ext) > 3 and image_ext != 'jpeg':
                    image_ext = image_ext[:3]
                if image_ext in ('jpg', 'png', 'gif', 'jpeg'):
                    image_name = html_content['image'].split('/')[-1]
                    image_hash = generate_hash()
                    image_hash_filename = '.'.join([image_hash, image_ext])
                    image_res_url = os.path.join(settings.MEDIA_URL, 'posts', image_hash_filename)

                    try:
                        req_image = requests.get(image_url, timeout=3)
                        im = Image.open(StringIO(req_image.content))
                        im.save(os.path.join(settings.MEDIA_ROOT, 'posts', image_hash_filename))
                        self.image_name = image_name
                        self.image_original_name = image_hash
                    except IOError:
                        logging.error('There was an error trying to retrieve the Image from the website %s' % url)
                        image_res_url = ''
                    except ConnectionError:
                        logging.error('There was an error in the connection')
                        image_res_url = ''

            text = self.content.replace(url, '')
            self.content = '''<img src="%s" class="img-polaroid post-image" />
                             &nbsp;<div><a href="%s" target="_blank">%s</a>
                             <p>%s</p></div><br /><span>%s</span>''' % (image_res_url, url,
                                                   html_content['title'],
                                                   html_content['description'],
                                                   text)
            self.save()

    def check_url(self):
        r = re.search('((https?:\/\/|www\.)[\w+\.]*\/?)', self.content)
        if r:
            url = r.group(0)
            if not url.startswith('http'):
                url = 'http://' + url
            try:
                validate = URLValidator(verify_exists=False)
                validate(url)
            except ValidationError:
                return None
        else:
            url = None

        return url

    def set_post_data(self):
        url = self.check_url()

        if url:
            self.get_content_url(url)


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, blank=True)
    task = models.ForeignKey(Task, null=True, blank=True)
    comment = models.ForeignKey('self', null=True, blank=True,
                                related_name='own_comments')
    text = models.TextField(db_column='comment')
    created_user = models.ForeignKey(User)
    created = models.DateTimeField(default=now(),
                                   null=True,
                                   blank=True)

    class Meta:
        db_table = u'comment'

    def __unicode__(self):
        return u'%s' % self.comment
