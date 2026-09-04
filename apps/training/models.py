from django.db import models
from django.utils import timezone


class TrainingRecord(models.Model):
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="training_records")
    employee_name = models.CharField(max_length=150)
    course_title = models.CharField(max_length=255)
    provider = models.CharField(max_length=255, blank=True)
    completed_on = models.DateField(default=timezone.now)
    expires_on = models.DateField(null=True, blank=True)
    certificate = models.FileField(upload_to="certificates/", blank=True, null=True)

    class Meta:
        ordering = ["-completed_on"]

    def __str__(self):
        return f"{self.employee_name} - {self.course_title}"

    @property
    def is_expired(self):
        return bool(self.expires_on and self.expires_on < timezone.now().date())


class FirstAiderMarshal(models.Model):
    class Role(models.TextChoices):
        FIRST_AIDER = "first_aider", "First aider"
        FIRE_MARSHAL = "fire_marshal", "Fire marshal"
        BOTH = "both", "First aider & Fire marshal"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="first_aiders")
    site = models.ForeignKey("organizations.Site", on_delete=models.SET_NULL, null=True, blank=True)
    employee_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FIRST_AIDER)
    certified_on = models.DateField(null=True, blank=True)
    certificate_expiry = models.DateField(null=True, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["employee_name"]

    def __str__(self):
        return self.employee_name


class OSHCommitteeMember(models.Model):
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="committee_members")
    employee_name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150, blank=True)
    represents = models.CharField(max_length=150, blank=True, help_text="Management or Workers")
    term_start = models.DateField(null=True, blank=True)
    term_end = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["employee_name"]

    def __str__(self):
        return self.employee_name
