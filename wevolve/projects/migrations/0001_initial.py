# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('type_field', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, db_column='type', blank=True)),
            ('image_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, null=True, blank=True)),
            ('image_original_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('licence', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Category'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 11, 15, 0, 0))),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 11, 15, 0, 0), null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['Project'])

        # Adding model 'ProjectPart'
        db.create_table(u'project_part', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('project_part', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.ProjectPart'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projectpart_created_user', to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 11, 15, 0, 0), null=True, blank=True)),
            ('modified_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='projectpart_modified_user', null=True, to=orm['users.User'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 11, 15, 0, 0), null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['ProjectPart'])

        # Adding model 'UserProject'
        db.create_table(u'user_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'], db_column='project_id')),
            ('permission', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='userproject_created_user', to=orm['users.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='userproject_modified_user', null=True, to=orm['users.User'])),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('projects', ['UserProject'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'project')

        # Deleting model 'ProjectPart'
        db.delete_table(u'project_part')

        # Deleting model 'UserProject'
        db.delete_table(u'user_project')


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
        'projects.userproject': {
            'Meta': {'object_name': 'UserProject', 'db_table': "u'user_project'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userproject_created_user'", 'to': "orm['users.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userproject_modified_user'", 'null': 'True', 'to': "orm['users.User']"}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']", 'db_column': "'project_id'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.User']"})
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

    complete_apps = ['projects']