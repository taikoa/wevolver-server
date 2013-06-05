# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Category.created'
        db.delete_column(u'category', 'created')

        # Deleting field 'Category.modified_user'
        db.delete_column(u'category', 'modified_user_id')

        # Deleting field 'Category.modified'
        db.delete_column(u'category', 'modified')

        # Deleting field 'Category.created_user'
        db.delete_column(u'category', 'created_user_id')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Category.created'
        raise RuntimeError("Cannot reverse this migration. 'Category.created' and its values cannot be restored.")
        # Adding field 'Category.modified_user'
        db.add_column(u'category', 'modified_user',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='category_modified_user', null=True, to=orm['auth.User'], blank=True),
                      keep_default=False)

        # Adding field 'Category.modified'
        db.add_column(u'category', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Category.created_user'
        raise RuntimeError("Cannot reverse this migration. 'Category.created_user' and its values cannot be restored.")

    models = {
        'home.category': {
            'Meta': {'object_name': 'Category', 'db_table': "u'category'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        },
        'home.country': {
            'Meta': {'object_name': 'Country', 'db_table': "u'country'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        }
    }

    complete_apps = ['home']