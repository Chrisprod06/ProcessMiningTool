from django.db import models
from django.forms import ModelForm
from django.conf import settings


# Create your models here.


class EventLog(models.Model):
    """Model to describe event logs"""
    event_log_id = models.AutoField(primary_key=True)
    event_log_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_log_name = models.CharField(max_length=100, default="event_log_name")
    event_log_file = models.FileField(upload_to="event_logs")

    def __str__(self):
        return self.event_log_name

    def delete(self, *args, **kwargs):
        self.event_log_file.delete()
        super().delete(*args, **kwargs)


class ProcessModel(models.Model):
    """Model to describe process models"""
    # Choices of algorithms for process discovery
    ALPHA_MINER = "alpha_miner"
    INDUCTIVE_MINER = "inductive_miner"
    HEURISTIC_MINER = "heuristic_miner"

    DISCOVERY_ALGORITHMS = [
        (ALPHA_MINER, "Alpha Miner"),
        (INDUCTIVE_MINER, "Inductive Miner"),
        (HEURISTIC_MINER, "Heuristic Miner")
    ]

    process_model_id = models.AutoField(primary_key=True)
    process_model_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    process_model_log_name = models.ForeignKey(EventLog, on_delete=models.CASCADE)
    process_model_name = models.CharField(max_length=100, default="process_model_name")
    process_model_algorithm = models.CharField(max_length=100, choices=DISCOVERY_ALGORITHMS)
    process_model_file = models.FileField(upload_to="process_models")

    def __str__(self):
        return self.process_model_name

    def delete(self, *args, **kwargs):
        self.process_model_file.delete()
        super().delete(*args, **kwargs)
