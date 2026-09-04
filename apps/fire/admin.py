from django.contrib import admin
from .models import FireEquipment


@admin.register(FireEquipment)
class FireEquipmentAdmin(admin.ModelAdmin):
    list_display = ("tag_number", "organization", "kind", "last_serviced", "next_service_due", "is_overdue")
    list_filter = ("organization", "kind")
