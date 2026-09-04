from django.contrib import admin
from .models import RiskAssessment, JobSafetyAnalysis, ToolboxTalk


@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ("activity", "organization", "status", "risk_score", "review_date")
    list_filter = ("organization", "status")


@admin.register(JobSafetyAnalysis)
class JSAAdmin(admin.ModelAdmin):
    list_display = ("task_name", "organization", "prepared_by", "created_at")
    list_filter = ("organization",)


@admin.register(ToolboxTalk)
class ToolboxTalkAdmin(admin.ModelAdmin):
    list_display = ("topic", "organization", "held_on", "attendees_count", "ai_generated")
    list_filter = ("organization", "ai_generated")
