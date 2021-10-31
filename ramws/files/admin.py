import datetime as dt

from django import forms
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Program, Run


class RunInline(admin.TabularInline):
    model = Run

    ordering = [
        "created_at",
    ]

    fields = [
        "input_name",
        "created_at",
    ]

    readonly_fields = [
        "input_name",
        "created_at",
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(created_by=request.user)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    ordering = [
        "name",
    ]

    search_fields = [
        "name",
        "code",
        "description",
    ]

    list_display = [
        "__str__",
        "description__ellipsis",
    ]

    fields = [
        "name",
        "description",
    ]

    inlines = [
        RunInline,
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs if request.user.is_superuser else qs.filter(authorized_users=request.user)
        )

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return (
            (list_display + ["code", "number_of_runs"])
            if request.user.is_superuser
            else list_display
        )

    def get_fields(self, request, obj):
        fields = super().get_fields(request, obj)
        return (fields + ["code"]) if request.user.is_superuser else fields

    @admin.display(description="Description")
    def description__ellipsis(self, obj):
        truncated = obj.description[:100]
        suffix = "..." if (len(truncated) < len(obj.description)) else ""
        return truncated + suffix

    @admin.display(description="# Runs")
    def number_of_runs(self, obj):
        return obj.runs.count()


class RunForm(forms.ModelForm):
    class Meta:
        model = Run

        fields = [
            "program",
        ]

    upload_input_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        program_qs = self.fields["program"].queryset

        if not request.user.is_superuser:
            self.fields["program"].queryset = program_qs.filter(
                authorized_users=request.user
            )

    def save(self, *args, **kwargs):
        input_file = self.cleaned_data.pop("upload_input_file")
        self.instance.input_file = input_file

        return super().save(*args, **kwargs)


class RunExtendedStatusListFilter(admin.SimpleListFilter):
    title = "status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            ("warning", "Warning"),
            ("ok", "OK"),
            ("pending_or_timeout", "Pending or Timeout"),
            ("client_error", "Client Error"),
            ("server_error", "Server Error"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        qs = queryset

        if value == "warning":
            qs = qs.filter(status=Run.Status.WARNING)

        elif value == "ok":
            qs = qs.filter(status=Run.Status.OK)

        elif value == "pending_or_timeout":
            qs = qs.filter(status=Run.Status.PENDING)

        elif value == "client_error":
            qs = qs.filter(status=Run.Status.CLIENT_ERROR)

        elif value == "server_error":
            qs = qs.filter(status=Run.Status.SERVER_ERROR)

        return qs


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display_links = None

    ordering = [
        "-created_at",
    ]

    search_fields = [
        "input_name",
        "program__name",
    ]

    list_display = [
        "input_name",
        "program",
        "created_at",
        "extended_status",
        "download_input_file",
        "download_output_file",
        "download_warnings_file",
    ]

    list_filter = [
        "program",
        "created_at",
        RunExtendedStatusListFilter,
    ]

    form = RunForm

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return (
            (list_display + ["download_logs_file", "created_by__linkified"])
            if request.user.is_superuser
            else list_display
        )

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        return (
            (list_filter + ["created_by"]) if request.user.is_superuser else list_filter
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(created_by=request.user)

    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super().get_form(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs["request"] = request
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        context["show_save_and_continue"] = False
        return super().render_change_form(request, context, add, change, form_url, obj)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="Status")
    def extended_status(self, obj):
        now = timezone.now()
        one_hour = dt.timedelta(hours=1)
        one_hour_ago = now - one_hour

        return (
            "Timeout"
            if ((obj.status == Run.Status.PENDING) and (obj.created_at < one_hour_ago))
            else obj.status
        )

    @staticmethod
    def formatted_download_html(href, enabled=True):
        if enabled:
            return format_html('<a href="{}">Download</a>', href)
        return format_html(
            '<span style="opacity: 0.5; cursor: not-allowed;">Download</span>'
        )

    @admin.display(description="Input")
    def download_input_file(self, obj):
        href = reverse("files:input-file", args=[obj.pk])

        return self.formatted_download_html(href)

    @admin.display(description="Output")
    def download_output_file(self, obj):
        href = reverse("files:output-file", args=[obj.pk])
        enabled = obj.status != Run.Status.PENDING

        return self.formatted_download_html(href, enabled)

    @admin.display(description="Logs")
    def download_logs_file(self, obj):
        href = reverse("files:logs-file", args=[obj.pk])
        enabled = obj.status != Run.Status.PENDING

        return self.formatted_download_html(href, enabled)

    @admin.display(description="Warnings")
    def download_warnings_file(self, obj):
        href = reverse("files:warnings-file", args=[obj.pk])
        enabled = obj.status != Run.Status.PENDING

        return self.formatted_download_html(href, enabled)

    @admin.display(description="Created by")
    def created_by__linkified(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:accounts_user_change", args=[obj.created_by.pk]),
            obj.created_by,
        )

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
