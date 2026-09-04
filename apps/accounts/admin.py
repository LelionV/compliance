from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Tenant", {"fields": ("role", "organization", "job_title", "phone")}),
    )
    list_display = ("username", "email", "role", "organization", "is_active")
    list_filter = ("role", "organization", "is_active")
