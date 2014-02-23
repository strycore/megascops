# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Video.page_title'
        db.delete_column(u'video_video', 'page_title')

        # Adding field 'Video.title'
        db.add_column(u'video_video', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True),
                      keep_default=False)


        # Changing field 'Video.host'
        db.alter_column(u'video_video', 'host', self.gf('django.db.models.fields.CharField')(default='', max_length=64))

    def backwards(self, orm):
        # Adding field 'Video.page_title'
        db.add_column(u'video_video', 'page_title',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Video.title'
        db.delete_column(u'video_video', 'title')


        # Changing field 'Video.host'
        db.alter_column(u'video_video', 'host', self.gf('django.db.models.fields.CharField')(max_length=64, null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'video.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size_quota': ('django.db.models.fields.IntegerField', [], {'default': '52428800'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'video_quota': ('django.db.models.fields.IntegerField', [], {'default': '5'})
        },
        u'video.video': {
            'Meta': {'object_name': 'Video'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'file_suffix': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['video.Profile']"}),
            'progress': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        }
    }

    complete_apps = ['video']