# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Document'
        db.create_table(u'document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectPart'])),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='document_created_user', to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='document_modified_user', null=True, to=orm['users.User'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('project_parts', ['Document'])

        # Adding model 'File'
        db.create_table(u'file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectPart'])),
            ('original_name', self.gf('django.db.models.fields.CharField')(max_length=765, null=True)),
            ('system_name', self.gf('django.db.models.fields.CharField')(max_length=765, null=True)),
            ('properties', self.gf('django.db.models.fields.CharField')(max_length=765, null=True)),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('project_parts', ['File'])

        # Adding model 'Post'
        db.create_table(u'post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectPart'])),
            ('type_field', self.gf('django.db.models.fields.IntegerField')(db_column='type')),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('image_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('image_original_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='post_created_user', to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('project_parts', ['Post'])

        # Adding model 'Session'
        db.create_table(u'session', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('data', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('lifetime', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('project_parts', ['Session'])

        # Adding model 'Comment'
        db.create_table(u'comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project_parts.Post'], null=True, blank=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Task'], null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='own_comments', null=True, to=orm['project_parts.Comment'])),
            ('text', self.gf('django.db.models.fields.TextField')(db_column='comment')),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('project_parts', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Document'
        db.delete_table(u'document')

        # Deleting model 'File'
        db.delete_table(u'file')

        # Deleting model 'Post'
        db.delete_table(u'post')

        # Deleting model 'Session'
        db.delete_table(u'session')

        # Deleting model 'Comment'
        db.delete_table(u'comment')


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
        'project_parts.comment': {
            'Meta': {'object_name': 'Comment', 'db_table': "u'comment'"},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'own_comments'", 'null': 'True', 'to': "orm['project_parts.Comment']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project_parts.Post']", 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'db_column': "'comment'"})
        },
        'project_parts.document': {
            'Meta': {'object_name': 'Document', 'db_table': "u'document'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'document_created_user'", 'to': "orm['users.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'document_modified_user'", 'null': 'True', 'to': "orm['users.User']"}),
            'project_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.ProjectPart']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'project_parts.file': {
            'Meta': {'object_name': 'File', 'db_table': "u'file'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'null': 'True'}),
            'project_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.ProjectPart']"}),
            'properties': ('django.db.models.fields.CharField', [], {'max_length': '765', 'null': 'True'}),
            'system_name': ('django.db.models.fields.CharField', [], {'max_length': '765', 'null': 'True'})
        },
        'project_parts.post': {
            'Meta': {'object_name': 'Post', 'db_table': "u'post'"},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_created_user'", 'to': "orm['users.User']"}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'image_original_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'project_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.ProjectPart']"}),
            'type_field': ('django.db.models.fields.IntegerField', [], {'db_column': "'type'"})
        },
        'project_parts.session': {
            'Meta': {'object_name': 'Session', 'db_table': "u'session'"},
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lifetime': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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

    complete_apps = ['project_parts']