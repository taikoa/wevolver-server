import os

from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from tastypie.utils import now

from wevolve.home.models import Category


class Project(models.Model):
    TYPE = ((2, 'CLOSED'), (1, 'PRIVATE'), (0, 'PUBLIC'))

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    type_field = models.IntegerField(db_column='type',
                                     null=True, blank=True, default=1,
                                     choices=TYPE)
    image_name = models.CharField(max_length=255, null=True, blank=True,
                                  default='')
    image_original_name = models.CharField(max_length=255, blank=True)
    licence = models.IntegerField(null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    categories = models.ManyToManyField(Category, null=True, blank=True)
    created = models.DateTimeField(default=now(), null=True, blank=True)
    created_user = models.ForeignKey(User)
    modified = models.DateTimeField(null=True, blank=True, default=now())
    drive_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = u'project'

    def __unicode__(self):
        return u'%d - %s' % (self.id, self.title)

    def build_tree(self, tree_object):
        parts = tree_object['object'].projectpart_set.all()

        if parts:
            tree_object['parts'] = [{'object': part, 'parts': []} for part in parts]
        else:
            return False

        for part in tree_object['parts']:
            self.build_tree(part)

    def get_tree_struct(self):
        root = self.projectpart_set.filter(project=self, project_part=None)
        root = root[0] or []

        tree_struct = [{'object': root, 'parts': []}]
        self.build_tree(tree_struct[0])

        return tree_struct

    def get_maxmin_activity(self):
        parts = self.projectpart_set.all()
        maximum = 0
        minimum = 100000000

        for part in parts:
            if part.progress() > maximum:
                maximum = part.progress()
            if part.progress() < minimum:
                minimum = part.progress()

        return (maximum, minimum)

    def get_image_name(self):
        if not self.image_name:
            return '/static/images/profile-img.gif'
        else:
            return os.path.join('/media/project',
                                self.image_name)

    def get_user_permission(self, user):
        if not user.is_authenticated():
            return False
        user_projects = User.objects.get(pk=user.id).userproject_set.filter(project=self.id)

        if user_projects:
            # user_project = user_projects[0]
            # return user_project.permission
            return True
        return False

    def members(self, user=None):
        members = [userproject.user for userproject in self.userproject_set.all()]
        members_out = []
        for member in members:
            if user.id != member.id:
                members_out.append({'id': member.id,
                                    'username': ' '.join([member.first_name, member.last_name]),
                                    'image_name': member.profile.get_image_profile(),
                                    'city': member.profile.city,
                                    'country': member.profile.country,
                                    'state': member.profile.state,
                                    'number_projects': member.userproject_set.count()
                                   })
        return members_out

    def is_open(self):
        return self.type_field == 0


class ProjectPart(models.Model):
    project = models.ForeignKey(Project)
    project_part = models.ForeignKey('self', null=True, blank=True)
    title = models.CharField(max_length=255)
    order = models.IntegerField(null=True)
    created_user = models.ForeignKey(User,
                                     related_name='projectpart_created_user')
    created = models.DateTimeField(null=True, blank=True, default=now())
    modified_user = models.ForeignKey(User, null=True, blank=True,
                                      related_name='projectpart_modified_user')
    modified = models.DateTimeField(null=True, blank=True, default=now())
    drive_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = u'project_part'

    def __unicode__(self):
        return u'%d - %s' % (self.id, self.title)

    def progress(self):
        return self.post_set.all().count() + self.task_count()

    def task_count(self):
        return self.task_set.all().count()

    def progress_done(self):
        return self.task_set.filter(flag_finished=1).count()

    def has_drive(self):
        return bool(self.drive_id)


class UserProjectManager(models.Manager):
    def check_perms(self, project, user):
        """@todo: Docstring for check_perms

        :project: @todo
        :user: @todo
        :returns: @todo

        """
        try:
            self.get(project=project, user=user, permission=1)
            return True
        except UserProject.DoesNotExist:
            return False


class UserProject(models.Model):
    CHOICES = ((1, 'ADMIN'), (0, 'USER'))

    user = models.ForeignKey(User)
    project = models.ForeignKey(Project, db_column='project_id')
    permission = models.IntegerField(max_length=2, default=0, choices=CHOICES)
    created_user = models.ForeignKey(User,
                                     related_name='userproject_created_user')
    created = models.DateTimeField(default=now(),
                                   null=True, blank=True)
    modified_user = models.ForeignKey(User, null=True, blank=True,
                                      related_name='userproject_modified_user')
    modified = models.DateTimeField(null=True, blank=True)
    drive_auth = models.BooleanField(default=False)

    objects = UserProjectManager()

    class Meta:
        db_table = u'user_project'

    def __unicode__(self):
        return u'%s' % self.id

    def is_admin(self):
        return self.permission == 1
