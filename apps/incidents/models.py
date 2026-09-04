from django.conf import settings
from django.db import models
from django.utils import timezone


class Incident(models.Model):
    class Kind(models.TextChoices):
        INJURY = "injury", "Injury"
        NEAR_MISS = "near_miss", "Near miss"
        PROPERTY = "property", "Property damage"
        ENVIRONMENTAL = "environmental", "Environmental"

    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical / LTI"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        INVESTIGATING = "investigating", "Investigating"
        AWAITING_DOSH = "awaiting_dosh", "Awaiting DOSH filing"
        CLOSED = "closed", "Closed"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="incidents")
    site = models.ForeignKey("organizations.Site", on_delete=models.SET_NULL, null=True, blank=True)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.NEAR_MISS)
    severity = models.CharField(max_length=10, choices=Severity.choices, default=Severity.LOW)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location_detail = models.CharField(max_length=255, blank=True)
    occurred_at = models.DateTimeField(default=timezone.now)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_lost_time_injury = models.BooleanField(default=False, help_text="Resets the LTI-free day counter")
    dosh_filed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_at"]

    def __str__(self):
        return f"{self.title} ({self.get_kind_display()})"
