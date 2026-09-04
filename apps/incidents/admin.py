from django.contrib import admin
from .models import Incident


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "kind", "severity", "status", "occurred_at", "dosh_filed")
    list_filter = ("organization", "kind", "severity", "status")
