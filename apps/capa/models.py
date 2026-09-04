from django.conf import settings
from django.db import models
from django.utils import timezone


class CorrectiveAction(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In progress"
        OVERDUE = "overdue", "Overdue"
        CLOSED = "closed", "Closed"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="capas")
    source_incident = models.ForeignKey("incidents.Incident", on_delete=models.SET_NULL, null=True, blank=True, related_name="capas")
    source_inspection = models.ForeignKey("inspections.Inspection", on_delete=models.SET_NULL, null=True, blank=True, related_name="capas")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(default=timezone.now)
    closed_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return self.status != self.Status.CLOSED and self.due_date < timezone.now().date()
