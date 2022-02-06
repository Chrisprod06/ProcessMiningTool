from django import forms
from django.forms import ModelForm

from .models import EventLog, ProcessModel


class EventLogForm(ModelForm):
    """Form used for handling event logs"""

    class Meta:
        model = EventLog
        fields = "__all__"


class ProcessModelForm(ModelForm):
    """Form used for upload/modify process models"""

    class Meta:
        model = ProcessModel
        fields = "__all__"


class DiscoverProcessModelForm(ModelForm):
    """Form used for discovering process models"""

    class Meta:
        model = ProcessModel
        fields = [
            "process_model_id",
            "process_model_owner",
            "process_model_log_name",
            "process_model_name",
            "process_model_algorithm",
        ]


class ConformanceCheckForm(forms.Form):
    """Form used for selecting process model and type of conformance"""

    TOKEN_REPLAY = "token_replay"

    CONFORMANCE_CHECKS_CHOICES = [
        (TOKEN_REPLAY, "Token Replay"),
    ]
    event_log = forms.ModelChoiceField(queryset=EventLog.objects.all())
    process_model = forms.ModelChoiceField(queryset=ProcessModel.objects.all())

    conformance_checks = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CONFORMANCE_CHECKS_CHOICES,
    )
