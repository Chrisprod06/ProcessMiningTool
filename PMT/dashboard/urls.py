from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index),

    path("process_discovery", views.process_discovery, name="process_discovery"),

    path("view_process_models", views.view_process_models, name="view_process_models"),
    path("view_process_models/delete/<int:pk>", views.delete_process_model, name="delete_process_model"),

    path("event_logs", views.event_logs, name="event_logs"),
    path("event_logs/delete/<int:pk>", views.delete_event_log, name="delete_event_log")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
