from django.conf import settings
from django.db import models
from django.utils import timezone


class AuditLogEntry(models.Model):
    class Action(models.TextChoices):
        CREATE = "create", "Created"
        UPDATE = "update", "Updated"
        DELETE = "delete", "Deleted"

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="audit_entries", null=True, blank=True
    )
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=Action.choices)
    model_label = models.CharField(max_length=100)
    object_repr = models.CharField(max_length=255)
    object_id = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = "Audit log entries"

    def __str__(self):
        return f"{self.get_action_display()} {self.model_label} #{self.object_id} by {self.actor}"
