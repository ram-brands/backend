from django.urls import include, path

from .views import admin_site, health_check, trigger_error

urlpatterns = [
    path("admin", admin_site.urls),
    path("error", trigger_error),
    path("", health_check),
    path("", include("accounts.urls")),
    path("", include("docs.urls")),
]
