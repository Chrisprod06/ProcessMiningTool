from django.contrib import admin

from .models import EventLog, ProcessModel

# Register your models here.
admin.site.register(EventLog)
admin.site.register(ProcessModel)
