# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'countries')


    def backwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'countries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150, unique=True)),
        ))
        db.send_create_signal('home', ['Country'])


    models = {
        'home.category': {
            'Meta': {'object_name': 'Category', 'db_table': "u'category'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '150'})
        }
    }

    complete_apps = ['home']
