from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from django.utils import dateformat, timezone
from tastypie.utils import now

from wevolve.projects.models import ProjectPart
from wevolve.project_parts.models import Comment


class ActivityManager(models.Manager):
    def set_activity(self, action, obj):
        entity_name = obj.__class__.__name__.lower()
        if entity_name == 'comment':
            if obj.task:
                project_part = obj.task.project_part
            elif obj.post:
                project_part = obj.post.project_part
        elif entity_name == 'projectpart':
            entity_name = 'part'
            project_part = obj
        else:
            project_part = obj.project_part

        activity_dict = {'action': action,
                         'entity': entity_name,
                         'project_part': project_part,
                         'related_id': obj.id,
                         'user': obj.created_user,
                         'created': obj.created
                         }
        activity = Activity(**activity_dict)
        activity.save()


class Activity(models.Model):
    ACTIONS = (('add', 'Add'), ('edit', 'Edit'),
               ('delete', 'Delete'))
    ENTITIES = (('task', 'Task'), ('post', 'Post'), ('document', 'Document'),
                ('part', 'Part'), ('comment', 'Comment'), ('file', 'File'))

    action = models.CharField(max_length=60, choices=ACTIONS)
    entity = models.CharField(max_length=60, choices=ENTITIES)
    user = models.ForeignKey(User)
    created = models.DateTimeField(default=now(), null=True,
                                   blank=True)
    project_part = models.ForeignKey(ProjectPart)
    related_id = models.IntegerField(max_length=30, null=True, blank=0,
                                     default=0)

    objects = ActivityManager()

    def __unicode__(self):
        return u'%s %s by %s' % (self.action, self.entity, self.user)

    def get_url(self):
        base_url = '/#/project/%d/parts/%d' % (self.project_part.project.id,
                                               self.project_part.id)
        if self.action == 'delete':
            return ''

        if self.entity == 'part':
            return base_url
        elif self.entity == 'comment':
            try:
                comment_data = Comment.objects.get(pk=self.related_id)
            except ObjectDoesNotExist:
                return ''

            related_entity = ''
            related_entity_id = 0

            if comment_data:
                if comment_data.task is not None:
                    related_entity = 'task'
                    related_entity_id = comment_data.task.id
                elif comment_data.post is not None:
                    related_entity = 'post'
                    related_entity_id = comment_data.post.id

            return '/'.join([base_url,
                             related_entity,
                             str(related_entity_id),
                             self.entity,
                             str(self.related_id),
                             ])
        else:
            return '/'.join([base_url, self.entity,
                             str(self.related_id)])

    def get_comment_data(self):
        if self.entity == 'comment':
            try:
                comment_obj = Comment.objects.get(pk=self.related_id)
                return model_to_dict(comment_obj)
            except ObjectDoesNotExist:
                return {}
        else:
            return {}

    def get_action_name(self):
        action_res = self.action
        if self.action.endswith('e'):
            action_res = ''.join([self.action, 'd'])
        else:
            action_res = ''.join([self.action, 'ed'])

        return action_res

    def get_created_date(self):
        today = now()

        if today.day == self.created.day:
            return ' - '.join(['today',
                               dateformat.format(timezone.localtime(self.created), 'H:i')])
        elif (today - timedelta(days=1)).date() == self.created.date():
            return ' - '.join(['yesterday',
                               dateformat.format(timezone.localtime(self.created), 'H:i')])
        else:
            return dateformat.format(timezone.localtime(self.created), 'jS F Y - H:i')

    def generate_activity(self):
        user = model_to_dict(self.user)
        user['username'] = ' '.join([user['first_name'], user['last_name']])

        return {'action': self.get_action_name(),
                'entity': self.entity,
                'id': self.id,
                'project_part': model_to_dict(self.project_part),
                'related_id': self.related_id,
                'username': user['username'],
                'comment_data': self.get_comment_data(),
                'url': self.get_url(),
                'created': self.get_created_date(),
                'project_title': self.project_part.project.title
                }
