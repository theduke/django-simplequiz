# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'django_simplequiz_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['django_simplequiz.Category'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'django_simplequiz', ['Category'])

        # Adding model 'Quiz'
        db.create_table(u'django_simplequiz_quiz', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_simplequiz.Category'], null=True, blank=True)),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('end_on_wrong_answers', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('force_order', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_paging', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('randomize_order', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('one_by_one', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ignore_case', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ignore_spaces', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('auto_accept', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_answers_on_finish', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('playcount', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'django_simplequiz', ['Quiz'])

        # Adding model 'Question'
        db.create_table(u'django_simplequiz_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['django_simplequiz.Quiz'])),
            ('kind', self.gf('django.db.models.fields.CharField')(default='plain', max_length=50)),
            ('name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('answer', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'django_simplequiz', ['Question'])

        # Adding model 'Attempt'
        db.create_table(u'django_simplequiz_attempt', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attempts', to=orm['django_simplequiz.Quiz'])),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('finished_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_taken', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('mistakes', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'django_simplequiz', ['Attempt'])

        # Adding model 'Challenge'
        db.create_table(u'django_simplequiz_challenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('challenger_attempt', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['django_simplequiz.Attempt'])),
            ('challenged', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('challenged_attempt', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['django_simplequiz.Attempt'])),
            ('challenged_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('declined', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'django_simplequiz', ['Challenge'])

        # Adding model 'QuizLike'
        db.create_table(u'django_simplequiz_quizlike', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(related_name='likes', to=orm['django_simplequiz.Quiz'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'django_simplequiz', ['QuizLike'])

        # Adding unique constraint on 'QuizLike', fields ['quiz', 'user']
        db.create_unique(u'django_simplequiz_quizlike', ['quiz_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'QuizLike', fields ['quiz', 'user']
        db.delete_unique(u'django_simplequiz_quizlike', ['quiz_id', 'user_id'])

        # Deleting model 'Category'
        db.delete_table(u'django_simplequiz_category')

        # Deleting model 'Quiz'
        db.delete_table(u'django_simplequiz_quiz')

        # Deleting model 'Question'
        db.delete_table(u'django_simplequiz_question')

        # Deleting model 'Attempt'
        db.delete_table(u'django_simplequiz_attempt')

        # Deleting model 'Challenge'
        db.delete_table(u'django_simplequiz_challenge')

        # Deleting model 'QuizLike'
        db.delete_table(u'django_simplequiz_quizlike')


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
        u'django_simplequiz.attempt': {
            'Meta': {'object_name': 'Attempt'},
            'finished_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mistakes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attempts'", 'to': u"orm['django_simplequiz.Quiz']"}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {}),
            'time_taken': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'django_simplequiz.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['django_simplequiz.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'django_simplequiz.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'challenged': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"}),
            'challenged_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'challenged_attempt': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['django_simplequiz.Attempt']"}),
            'challenger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"}),
            'challenger_attempt': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['django_simplequiz.Attempt']"}),
            'declined': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'django_simplequiz.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "'plain'", 'max_length': '50'}),
            'name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['django_simplequiz.Quiz']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'django_simplequiz.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'allow_paging': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'auto_accept': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_simplequiz.Category']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_on_wrong_answers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'force_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignore_case': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ignore_spaces': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'one_by_one': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'playcount': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'randomize_order': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_answers_on_finish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'django_simplequiz.quizlike': {
            'Meta': {'unique_together': "(('quiz', 'user'),)", 'object_name': 'QuizLike'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'likes'", 'to': u"orm['django_simplequiz.Quiz']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['django_simplequiz']