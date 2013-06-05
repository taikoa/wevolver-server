# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table(u'task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectPart'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('skill', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='skill_id')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], null=True, db_column='user_id')),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('flag_finished', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='task_created_user', to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='task_modified_user', null=True, to=orm['users.User'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('tasks', ['Task'])

        # Adding model 'TaskSkill'
        db.create_table(u'task_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Skill'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taskskill_created_user', to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_user_id1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='taskskill_modified_user', null=True, db_column='modified_user_id1', to=orm['users.User'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('tasks', ['TaskSkill'])

        # Adding model 'TaskUser'
        db.create_table(u'task_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taskuser_created_user', to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='taskuser_modified_user', null=True, to=orm['users.User'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('tasks', ['TaskUser'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table(u'task')

        # Deleting model 'TaskSkill'
        db.delete_table(u'task_skill')

        # Deleting model 'TaskUser'
        db.delete_table(u'task_user')


    models = {
        'home.category': {
            'Meta': {'object_name': 'Category', 'db_table': "u'category'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'category_created_user'", 'to': "orm['users.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category_modified_user'", 'null': 'True', 'to': "orm['users.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project', 'db_table': "u'project'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.Category']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 15, 0, 0)'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_original_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'licence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 15, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'type_field': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'db_column': "'type'", 'blank': 'True'})
        },
        'projects.projectpart': {
            'Meta': {'object_name': 'ProjectPart', 'db_table': "u'project_part'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 15, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projectpart_created_user'", 'to': "orm['users.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 15, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projectpart_modified_user'", 'null': 'True', 'to': "orm['users.User']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"}),
            'project_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.ProjectPart']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'tasks.task': {
            'Meta': {'object_name': 'Task', 'db_table': "u'task'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'task_created_user'", 'to': "orm['users.User']"}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'flag_finished': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task_modified_user'", 'null': 'True', 'to': "orm['users.User']"}),
            'project_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.ProjectPart']"}),
            'skill': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'skill_id'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'null': 'True', 'db_column': "'user_id'"})
        },
        'tasks.taskskill': {
            'Meta': {'object_name': 'TaskSkill', 'db_table': "u'task_skill'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taskskill_created_user'", 'to': "orm['users.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user_id1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taskskill_modified_user'", 'null': 'True', 'db_column': "'modified_user_id1'", 'to': "orm['users.User']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Skill']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'tasks.taskuser': {
            'Meta': {'object_name': 'TaskUser', 'db_table': "u'task_user'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taskuser_created_user'", 'to': "orm['users.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taskuser_modified_user'", 'null': 'True', 'to': "orm['users.User']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"})
        },
        'users.skill': {
            'Meta': {'object_name': 'Skill', 'db_table': "u'skill'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skill_created_user'", 'to': "orm['users.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'skill_modified_user'", 'null': 'True', 'to': "orm['users.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        'users.user': {
            'Meta': {'object_name': 'User', 'db_table': "u'user'"},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'country_id'"}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']", 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'picture_original_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'skills': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['tasks']