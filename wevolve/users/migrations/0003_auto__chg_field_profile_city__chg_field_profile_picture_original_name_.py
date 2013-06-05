# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Profile.city'
        db.alter_column(u'user_profile', 'city', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Profile.picture_original_name'
        db.alter_column(u'user_profile', 'picture_original_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Profile.interests'
        db.alter_column(u'user_profile', 'interests', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Profile.skills'
        db.alter_column(u'user_profile', 'skills', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Profile.country'
        db.alter_column(u'user_profile', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Country'], null=True, db_column='country_id'))
        # Adding index on 'Profile', fields ['country']
        db.create_index(u'user_profile', ['country_id'])


        # Changing field 'Profile.token'
        db.alter_column(u'user_profile', 'token', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Profile.state'
        db.alter_column(u'user_profile', 'state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Profile.status'
        db.alter_column(u'user_profile', 'status', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Profile.bio'
        db.alter_column(u'user_profile', 'bio', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Profile.data'
        db.alter_column(u'user_profile', 'data', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Skill.created'
        db.alter_column(u'skill', 'created', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'UserSkill.created'
        db.alter_column(u'user_skill', 'created', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Removing index on 'Profile', fields ['country']
        db.delete_index(u'user_profile', ['country_id'])


        # Changing field 'Profile.city'
        db.alter_column(u'user_profile', 'city', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Profile.picture_original_name'
        db.alter_column(u'user_profile', 'picture_original_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Profile.interests'
        db.alter_column(u'user_profile', 'interests', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Profile.skills'
        db.alter_column(u'user_profile', 'skills', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Profile.country'
        db.alter_column(u'user_profile', 'country_id', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='country_id'))

        # Changing field 'Profile.token'
        db.alter_column(u'user_profile', 'token', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Profile.state'
        db.alter_column(u'user_profile', 'state', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Profile.status'
        db.alter_column(u'user_profile', 'status', self.gf('django.db.models.fields.IntegerField')(default=0))

        # Changing field 'Profile.bio'
        db.alter_column(u'user_profile', 'bio', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Profile.data'
        db.alter_column(u'user_profile', 'data', self.gf('django.db.models.fields.TextField')(default=' '))

        # Changing field 'Skill.created'
        db.alter_column(u'skill', 'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 3, 0, 0)))

        # Changing field 'UserSkill.created'
        db.alter_column(u'user_skill', 'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 3, 0, 0)))

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
        'home.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'country'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        'users.profile': {
            'Meta': {'object_name': 'Profile', 'db_table': "u'user_profile'"},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.Country']", 'null': 'True', 'db_column': "'country_id'"}),
            'data': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Profile']", 'null': 'True', 'blank': 'True'}),
            'picture_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'picture_original_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'skills': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True'})
        },
        'users.skill': {
            'Meta': {'object_name': 'Skill', 'db_table': "u'skill'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 3, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skill_created_user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'skill_modified_user'", 'null': 'True', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        'users.userskill': {
            'Meta': {'object_name': 'UserSkill', 'db_table': "u'user_skill'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 3, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'userskill_created_user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user_id1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'userskill_modified_user'", 'null': 'True', 'db_column': "'modified_user_id1'", 'to': "orm['auth.User']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Skill']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['users']