from django.contrib import admin
from .models import Organization, Site, ComplianceItem


class SiteInline(admin.TabularInline):
    model = Site
    extra = 1


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "dosh_reg_no", "industry", "seats", "is_active", "compliance_score")
    search_fields = ("name", "dosh_reg_no")
    inlines = [SiteInline]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ComplianceItem)
class ComplianceItemAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "is_evidenced", "last_reviewed")
    list_filter = ("organization", "is_evidenced")
