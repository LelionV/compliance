from django.conf import settings
from django.db import models
from django.utils import timezone


class RiskAssessment(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        DUE_REVIEW = "due_review", "Due for review"
        EXPIRED = "expired", "Expired"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="risk_assessments")
    site = models.ForeignKey("organizations.Site", on_delete=models.SET_NULL, null=True, blank=True)
    activity = models.CharField(max_length=255)
    hazards_identified = models.TextField(blank=True)
    existing_controls = models.TextField(blank=True)
    likelihood = models.PositiveSmallIntegerField(default=1, help_text="1 (rare) - 5 (almost certain)")
    severity = models.PositiveSmallIntegerField(default=1, help_text="1 (negligible) - 5 (catastrophic)")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    assessed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    review_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def risk_score(self):
        return self.likelihood * self.severity

    def __str__(self):
        return self.activity


class JobSafetyAnalysis(models.Model):
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="jsas")
    task_name = models.CharField(max_length=255)
    steps = models.TextField(help_text="One step per line")
    hazards = models.TextField(blank=True)
    ppe_required = models.CharField(max_length=255, blank=True)
    prepared_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.task_name


class ToolboxTalk(models.Model):
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="toolbox_talks")
    site = models.ForeignKey("organizations.Site", on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    facilitator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    attendees_count = models.PositiveIntegerField(default=0)
    held_on = models.DateField(default=timezone.now)
    ai_generated = models.BooleanField(default=False, help_text="Generated via AI toolbox talk assistant")

    class Meta:
        ordering = ["-held_on"]

    def __str__(self):
        return f"{self.topic} - {self.held_on}"
