from django.urls import path

from .views import confirmation, input_file, output_file

app_name = "files"

urlpatterns = [
    path("runs/<uuid:pk>/input_file", input_file, name="input-file"),
    path("runs/<uuid:pk>/output_file", output_file, name="output-file"),
    path("runs/<uuid:pk>/confirmation", confirmation, name="confirmation"),
]
