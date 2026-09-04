from django.contrib import admin
from .models import TrainingRecord, FirstAiderMarshal, OSHCommitteeMember


@admin.register(TrainingRecord)
class TrainingRecordAdmin(admin.ModelAdmin):
    list_display = ("employee_name", "course_title", "organization", "completed_on", "expires_on")
    list_filter = ("organization",)


@admin.register(FirstAiderMarshal)
class FirstAiderMarshalAdmin(admin.ModelAdmin):
    list_display = ("employee_name", "organization", "role", "certificate_expiry")
    list_filter = ("organization", "role")


@admin.register(OSHCommitteeMember)
class OSHCommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ("employee_name", "organization", "designation", "represents")
    list_filter = ("organization",)
