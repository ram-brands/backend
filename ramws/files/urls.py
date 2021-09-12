from django.urls import path

from .views import confirmation, input_file, logs_file, output_file, warnings_file

app_name = "files"

urlpatterns = [
    path("runs/<uuid:pk>/input_file", input_file, name="input-file"),
    path("runs/<uuid:pk>/output_file", output_file, name="output-file"),
    path("runs/<uuid:pk>/logs_file", logs_file, name="logs-file"),
    path("runs/<uuid:pk>/warnings_file", warnings_file, name="warnings-file"),
    path("runs/<uuid:pk>/confirmation", confirmation, name="confirmation"),
]
