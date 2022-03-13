from django.forms import ModelForm
from django import forms

from .models import EventLog, ProcessModel


class EventLogForm(ModelForm):
    """Form used for handling event logs"""

    class Meta:
        model = EventLog
        fields = "__all__"



class CustomEventLogModelChoiceField(forms.ModelChoiceField):
    """Class to return text the name but value the id"""

    def label_from_instance(self, object):
        return object.event_log_name


class SelectEventLogForm(forms.Form):
    """Form used for selecting event log"""
    event_log = CustomEventLogModelChoiceField(queryset=EventLog.objects.all())
