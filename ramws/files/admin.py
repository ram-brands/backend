from django import forms
from django.conf import settings
from django.contrib import admin

from .models import Program, Run


import logging
logger = logging.getLogger(__name__)


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
        "description",
    ]

    list_display = [
        "__str__",
        "number_of_runs",
    ]

    fields = [
        "name",
        "description",
    ]

    inlines = [
        RunInline,
    ]

    @admin.display(description="# Runs")
    def number_of_runs(self, obj):
        return obj.runs.count()


class RunForm(forms.ModelForm):
    class Meta:
        model = Run

        fields = [
            "program",
        ]

        # readonly_fields = [
        #     "input_name",
        #     "program",
        #     "created_at"
        # ]

    input_file = forms.FileField()

    def save(self, *args, **kwargs):
        input_file = self.cleaned_data["input_file"]
        self.instance.input_file = input_file

        return super().save(*args, **kwargs)


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    ordering = [
        "-created_at",
    ]

    search_fields = [
        "input_name",
        "program__name",
    ]

    list_display = [
        "__str__",
        "program",
        "created_at",
        "status",
    ]

    list_filter = [
        "program",
        "created_at",
        "status",
    ]

    form = RunForm

    # def has_add_permission(self, request):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
