from django.urls import include, path

from .views import admin_site, health_check, trigger_error

urlpatterns = [
    path("", admin_site.urls, name="admin"),
    path("error", trigger_error, name="error"),
    path("health", health_check, name="health"),
    path("", include("accounts.urls")),
    path("", include("docs.urls")),
    path("", include("files.urls")),
]
