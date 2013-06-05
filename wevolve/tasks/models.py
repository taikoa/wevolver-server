from django.db import models
from django.contrib.auth.models import User
from tastypie.utils import now

from wevolve.projects.models import ProjectPart
from wevolve.users.models import Skill


class Task(models.Model):
    project_part = models.ForeignKey(ProjectPart)
    description = models.TextField()
    skill = models.IntegerField(null=True, db_column='skill_id')
    user = models.ForeignKey(User, null=True, db_column='user_id')
    deadline = models.DateTimeField(null=True, blank=True)
    flag_finished = models.IntegerField(max_length=1, default=0)
    created_user = models.ForeignKey(User, related_name='task_created_user')
    created = models.DateTimeField(null=True, blank=True,
                                   default=now())
    modified_user = models.ForeignKey(User, null=True,
                                      blank=True,
                                      related_name='task_modified_user')
    modified = models.DateTimeField(null=True, blank=True)
    weight = models.IntegerField(max_length=255, default=0)

    class Meta:
        db_table = u'task'

    def __unicode__(self):
        return u'%s' % self.description

    def get_absolute_url(self):
        return '/'.join(['/#/project', str(self.project_part.project.id),
                         'parts', str(self.project_part.id), 'task',
                         str(self.id)])


class TaskSkill(models.Model):
    skill = models.ForeignKey(Skill)
    task = models.ForeignKey(Task)
    created_user = models.ForeignKey(User,
                                     related_name='taskskill_created_user')
    created = models.DateTimeField(null=True, blank=True,
                                   default=now())
    modified_user_id1 = models.ForeignKey(User, null=True,
                                          db_column='modified_user_id1',
                                          blank=True,
                                          related_name='taskskill_modified_user')
    modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'task_skill'


class TaskUser(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    created_user = models.ForeignKey(User, related_name='taskuser_created_user')
    created = models.DateTimeField(null=True, blank=True,
                                   default=now())
    modified_user = models.ForeignKey(User, null=True,
                                      blank=True,
                                      related_name='taskuser_modified_user')
    modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = u'task_user'
