from django.contrib import admin
from .models import Inspection


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "status", "scheduled_date", "completed_date")
    list_filter = ("organization", "status")
