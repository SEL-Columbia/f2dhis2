from django.contrib import admin

from main.models import DataElement, DataSet, DataValueSet, FormDataElement, FormhubService

admin.site.register(DataElement)
admin.site.register(DataSet)
admin.site.register(DataValueSet)
admin.site.register(FormDataElement)
admin.site.register(FormhubService)