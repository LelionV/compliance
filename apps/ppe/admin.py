from django.contrib import admin
from .models import PPEItem, PPEIssuance


@admin.register(PPEItem)
class PPEItemAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "category", "stock_quantity", "reorder_level")
    list_filter = ("organization", "category")


@admin.register(PPEIssuance)
class PPEIssuanceAdmin(admin.ModelAdmin):
    list_display = ("item", "employee_name", "organization", "quantity", "issued_on")
    list_filter = ("organization",)
