from django.contrib import admin
from .models import CorrectiveAction


@admin.register(CorrectiveAction)
class CorrectiveActionAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "priority", "status", "due_date", "is_overdue")
    list_filter = ("organization", "priority", "status")
