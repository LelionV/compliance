from django.conf import settings
from django.db import models
from django.utils import timezone


class DOSHSReport(models.Model):
    class Kind(models.TextChoices):
        ANNUAL_RETURN = "annual_return", "Annual return"
        INCIDENT_FILING = "incident_filing", "Incident filing (DOSH 1)"
        DOSHS_PACK = "doshs_pack", "DOSHS compliance pack"
        OTHER = "other", "Other"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="doshs_reports")
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.DOSHS_PACK)
    title = models.CharField(max_length=255)
    generated_pdf = models.FileField(upload_to="doshs_reports/", blank=True, null=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    generated_at = models.DateTimeField(default=timezone.now)
    submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return self.title


class StatutoryDeadline(models.Model):
    """Powers the compliance calendar / 'Statutory deadlines' widget."""
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        DUE_SOON = "due_soon", "Due soon"
        OVERDUE = "overdue", "Overdue"
        DONE = "done", "Done"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="deadlines")
    title = models.CharField(max_length=255)
    statutory_reference = models.CharField(max_length=255, blank=True, help_text="e.g. Fire Risk Reduction Rules 2007")
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    notify_email = models.BooleanField(default=True)
    notify_sms = models.BooleanField(default=True)

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.title} ({self.due_date})"

    def computed_status(self):
        today = timezone.now().date()
        if self.status == self.Status.DONE:
            return self.Status.DONE
        if self.due_date < today:
            return self.Status.OVERDUE
        if (self.due_date - today).days <= 14:
            return self.Status.DUE_SOON
        return self.Status.SCHEDULED
