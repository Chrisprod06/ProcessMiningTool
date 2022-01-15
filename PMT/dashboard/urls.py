from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index),
    path("process_discovery", views.process_discovery, name="process_discovery"),
    path("event_logs", views.event_logs, name="event_logs"),
    path("event_logs/delete/<int:pk>", views.delete_event_log, name="delete_event_log"),
    path("event_logs/update/<int:pk>", views.modify_event_log, name="modify_event_log")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
