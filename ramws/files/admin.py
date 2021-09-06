from django import forms
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
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
        "code",
        "ellipsis_description",
        "number_of_runs",
    ]

    fields = [
        "name",
        "code",
        "description",
    ]

    inlines = [
        RunInline,
    ]

    @admin.display(description="Description")
    def ellipsis_description(self, obj):
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

    def save(self, *args, **kwargs):
        input_file = self.cleaned_data.pop("upload_input_file")
        self.instance.input_file = input_file

        return super().save(*args, **kwargs)


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
        "status",
        "download_input_file",
        "download_output_file",
    ]

    list_filter = [
        "program",
        "created_at",
        "status",
    ]

    form = RunForm

    @admin.display(description="Input file")
    def download_input_file(self, obj):
        return format_html(
            '<a href="{}">Download</a>', reverse("files:input-file", args=[obj.pk])
        )

    @admin.display(description="Output file")
    def download_output_file(self, obj):
        return format_html(
            '<a href="{}">Download</a>', reverse("files:output-file", args=[obj.pk])
        )

    def has_view_permission(self, request, obj=None):
        return obj is None

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
