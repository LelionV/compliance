from django.contrib import admin
from .models import DOSHSReport, StatutoryDeadline


@admin.register(DOSHSReport)
class DOSHSReportAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "kind", "generated_at", "submitted")
    list_filter = ("organization", "kind", "submitted")


@admin.register(StatutoryDeadline)
class StatutoryDeadlineAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "due_date", "status")
    list_filter = ("organization", "status")
