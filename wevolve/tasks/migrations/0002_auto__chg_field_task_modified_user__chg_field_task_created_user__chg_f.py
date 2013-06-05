# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Task.modified_user'
        db.alter_column(u'task', 'modified_user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'Task.created_user'
        db.alter_column(u'task', 'created_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Task.user'
        db.alter_column(u'task', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, db_column='user_id'))

        # Changing field 'TaskUser.modified_user'
        db.alter_column(u'task_user', 'modified_user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'TaskUser.created_user'
        db.alter_column(u'task_user', 'created_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'TaskUser.user'
        db.alter_column(u'task_user', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'TaskSkill.created_user'
        db.alter_column(u'task_skill', 'created_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'TaskSkill.modified_user_id1'
        db.alter_column(u'task_skill', 'modified_user_id1', self.gf('django.db.models.fields.related.ForeignKey')(null=True, db_column='modified_user_id1', to=orm['auth.User']))

    def backwards(self, orm):

        # Changing field 'Task.modified_user'
        db.alter_column(u'task', 'modified_user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['users.User']))

        # Changing field 'Task.created_user'
        db.alter_column(u'task', 'created_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User']))

        # Changing field 'Task.user'
        db.alter_column(u'task', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], null=True, db_column='user_id'))

        # Changing field 'TaskUser.modified_user'
        db.alter_column(u'task_user', 'modified_user_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['users.User']))

        # Changing field 'TaskUser.created_user'
        db.alter_column(u'task_user', 'created_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User']))

        # Changing field 'TaskUser.user'
        db.alter_column(u'task_user', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User']))

        # Changing field 'TaskSkill.created_user'
        db.alter_column(u'task_skill', 'created_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User']))

        # Changing field 'TaskSkill.modified_user_id1'
        db.alter_column(u'task_skill', 'modified_user_id1', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['users.User'], db_column='modified_user_id1'))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'home.category': {
            'Meta': {'object_name': 'Category', 'db_table': "u'category'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'category_created_user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category_modified_user'", 'null': 'True', 'to': "orm['auth.User']"}),
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
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projectpart_created_user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 15, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projectpart_modified_user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"}),
            'project_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.ProjectPart']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'tasks.task': {
            'Meta': {'object_name': 'Task', 'db_table': "u'task'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'task_created_user'", 'to': "orm['auth.User']"}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'flag_finished': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'task_modified_user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'project_part': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.ProjectPart']"}),
            'skill': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'skill_id'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'db_column': "'user_id'"})
        },
        'tasks.taskskill': {
            'Meta': {'object_name': 'TaskSkill', 'db_table': "u'task_skill'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taskskill_created_user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user_id1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taskskill_modified_user'", 'null': 'True', 'db_column': "'modified_user_id1'", 'to': "orm['auth.User']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Skill']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"})
        },
        'tasks.taskuser': {
            'Meta': {'object_name': 'TaskUser', 'db_table': "u'task_user'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taskuser_created_user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taskuser_modified_user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'users.skill': {
            'Meta': {'object_name': 'Skill', 'db_table': "u'skill'"},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skill_created_user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'skill_modified_user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        }
    }

    complete_apps = ['tasks']