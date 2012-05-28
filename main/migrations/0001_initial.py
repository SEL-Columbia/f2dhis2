# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FormhubService'
        db.create_table('dhis_formhub_servicet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('id_string', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('json', self.gf('django.db.models.fields.TextField')()),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('main', ['FormhubService'])

        # Adding model 'DataSet'
        db.create_table('dhis_data_set', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_set_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('main', ['DataSet'])

        # Adding model 'DataValueSet'
        db.create_table('dhis_data_value_set', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.FormhubService'])),
            ('org_unit', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('data_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.DataSet'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('main', ['DataValueSet'])

        # Adding model 'DataElement'
        db.create_table('dhis_data_element', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_element_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('data_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.DataSet'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('main', ['DataElement'])

        # Adding model 'FormDataElement'
        db.create_table('dhis_form_data_element', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_value_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.DataValueSet'])),
            ('data_element', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.DataElement'])),
            ('form_field', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('main', ['FormDataElement'])

        # Adding unique constraint on 'FormDataElement', fields ['data_value_set', 'data_element']
        db.create_unique('dhis_form_data_element', ['data_value_set_id', 'data_element_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FormDataElement', fields ['data_value_set', 'data_element']
        db.delete_unique('dhis_form_data_element', ['data_value_set_id', 'data_element_id'])

        # Deleting model 'FormhubService'
        db.delete_table('dhis_formhub_servicet')

        # Deleting model 'DataSet'
        db.delete_table('dhis_data_set')

        # Deleting model 'DataValueSet'
        db.delete_table('dhis_data_value_set')

        # Deleting model 'DataElement'
        db.delete_table('dhis_data_element')

        # Deleting model 'FormDataElement'
        db.delete_table('dhis_form_data_element')


    models = {
        'main.dataelement': {
            'Meta': {'object_name': 'DataElement', 'db_table': "'dhis_data_element'"},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_element_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.DataSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'main.dataset': {
            'Meta': {'object_name': 'DataSet', 'db_table': "'dhis_data_set'"},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_set_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'main.datavalueset': {
            'Meta': {'object_name': 'DataValueSet', 'db_table': "'dhis_data_value_set'"},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.DataSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'org_unit': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.FormhubService']"})
        },
        'main.formdataelement': {
            'Meta': {'unique_together': "(('data_value_set', 'data_element'),)", 'object_name': 'FormDataElement', 'db_table': "'dhis_form_data_element'"},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.DataElement']"}),
            'data_value_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.DataValueSet']"}),
            'form_field': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'main.formhubservice': {
            'Meta': {'object_name': 'FormhubService', 'db_table': "'dhis_formhub_servicet'"},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_string': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'json': ('django.db.models.fields.TextField', [], {}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['main']
