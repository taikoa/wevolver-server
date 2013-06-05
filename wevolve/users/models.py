import os

from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from tastypie.utils import now


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, unique=True)
    picture_name = models.CharField(max_length=255, blank=True, null=True)
    picture_original_name = models.CharField(max_length=255, blank=True,
                                             null=True)
    country = models.CharField(max_length=255, default='None')
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255,
                             blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    status = models.IntegerField(null=True, default=0)
    token = models.CharField(max_length=255, blank=True, null=True)
    modified = models.DateTimeField(null=True, blank=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    drive_id = models.CharField(max_length=100, blank=True, null=True)
    drive_token = models.TextField(blank=True, null=True)
    drive_folder = models.CharField(max_length=755, blank=True, null=True)

    class Meta:
        db_table = u'user_profile'

    def get_complete_name(self):
        return ' '.join([self.user.first_name, self.user.last_name])

    def get_image_profile(self):
        if not self.picture_name:
            return '/static/images/profile-img.gif'
        else:
            return os.path.join('/media/user',
                                self.picture_name)

    def projects(self, user=None):
        projects = [userproject.project for userproject in self.user.userproject_set.all()]
        projects_out = []
        for project in projects:
            project_aux = {'id': project.id,
                           'title': project.title,
                           'description': project.description,
                           'tags': project.tags,
                           'categories': [model_to_dict(category) for category in project.categories.all()],
                           'image_name': project.get_image_name()}
            if user:
                project_aux['auth'] = project.get_user_permission(user)
            projects_out.append(project_aux)

        return projects_out

    def __unicode__(self):
        return u'%s %s profile' % (self.user.first_name, self.user.last_name)


class Skill(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_user = models.ForeignKey(User, related_name='skill_created_user')
    created = models.DateTimeField(null=True, blank=True, default=now())
    modified_user = models.ForeignKey(User, null=True, blank=True,
                                      related_name='skill_modified_user')
    modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'skill'


class UserSkill(models.Model):
    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
    created_user = models.ForeignKey(User, related_name='userskill_created_user')
    created = models.DateTimeField(null=True, blank=True, default=now())
    modified_user_id1 = models.ForeignKey(User, null=True,
                                          db_column='modified_user_id1', blank=True,
                                          related_name='userskill_modified_user')
    modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'user_skill'
