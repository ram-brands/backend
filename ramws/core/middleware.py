from django.conf import settings
from django.middleware.common import CommonMiddleware as BaseCommonMiddleware
from django.urls import reverse


class CommonMiddleware(BaseCommonMiddleware):
    def process_request(self, request):
        """
        Always allow health checks, regardless of host.
        """
        health_check_path = reverse("health")
        request_path = request.get_full_path()

        user_agent = request.META.get("HTTP_USER_AGENT")

        if not (
            (health_check_path == request_path)
            and (user_agent in settings.ALLOWED_HEALTH_CHECK_USER_AGENTS)
        ):
            return super().process_request(request)
