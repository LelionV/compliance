from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "organization", "level", "is_read", "created_at")
    list_filter = ("organization", "level", "is_read")
