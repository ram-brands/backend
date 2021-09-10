from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = [
        "last_name",
        "first_name",
    ]

    search_fields = [
        "email",
        "first_name",
        "last_name",
    ]

    list_display = [
        "__str__",
        "full_name",
        "is_staff",
        "is_superuser",
        "date_joined",
    ]

    list_filter = [
        "is_staff",
        "is_superuser",
        "date_joined",
    ]

    fieldsets = [
        (
            "PERMISSIONS",
            {
                "fields": [
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "authorized_programs",
                ],
            },
        ),
        (
            "PERSONAL",
            {
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                ],
            },
        ),
    ]

    add_fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]

    filter_horizontal = ["groups", "user_permissions", "authorized_programs"]
