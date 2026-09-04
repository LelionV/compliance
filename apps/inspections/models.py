from django.conf import settings
from django.db import models
from django.utils import timezone


class Inspection(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="inspections")
    site = models.ForeignKey("organizations.Site", on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    checklist_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    scheduled_date = models.DateField(default=timezone.now)
    completed_date = models.DateField(null=True, blank=True)
    inspector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    signature_image = models.ImageField(upload_to="signatures/inspections/", blank=True, null=True)

    class Meta:
        ordering = ["-scheduled_date"]

    def __str__(self):
        return self.title
