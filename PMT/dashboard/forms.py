from django import forms
from django.forms import ModelForm

from .models import EventLog


class EventLogForm(ModelForm):
    """Form used for handling event logs"""
    class Meta:
        model = EventLog
        fields = ["event_log_name", "event_log_id", "event_log_owner", "event_log_file"]
