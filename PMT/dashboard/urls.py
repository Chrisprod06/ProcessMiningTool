from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("view_process_models", views.view_process_models, name="view_process_models"),
    path(
        "view_process_models/delete/<int:pk>",
        views.delete_process_model,
        name="delete_process_model",
    ),
    path("view_process_models/visualize/<int:pk>", views.visualize_process_model, name="visualize_process_model"),

    path("view_event_logs", views.view_event_logs, name="view_event_logs"),
    path("view_event_logs/delete/<int:pk>", views.delete_event_log, name="delete_event_log"),

    path("view_statistics/performance_dashboard/<int:pk>", views.view_performance_dashboard,
         name="view_performance_dashboard"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
