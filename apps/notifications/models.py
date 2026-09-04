from django.conf import settings
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    class Level(models.TextChoices):
        INFO = "info", "Info"
        WARNING = "warning", "Warning"
        DANGER = "danger", "Danger"

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="notifications"
    )
    # If user is null, it's a broadcast to everyone in the organization (all org
    # staff + any platform admin currently viewing that org).
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="notifications"
    )
    level = models.CharField(max_length=10, choices=Level.choices, default=Level.INFO)
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.message

    @classmethod
    def notify_organization(cls, organization, message, level=Level.INFO, link=""):
        return cls.objects.create(organization=organization, message=message, level=level, link=link)
