from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        PLATFORM_ADMIN = "platform_admin", "Platform Admin (Auditor)"
        ORG_ADMIN = "org_admin", "Organization Admin (Safety & Health Officer)"
        ORG_STAFF = "org_staff", "Organization Staff"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ORG_STAFF)
    job_title = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30, blank=True)

    # Org users belong to exactly one organization. Platform admins have none set
    # (they switch between organizations via session instead).
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )

    @property
    def is_platform_admin(self):
        return self.role == self.Role.PLATFORM_ADMIN or self.is_superuser

    def __str__(self):
        return self.get_full_name() or self.username
