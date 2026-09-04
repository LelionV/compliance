from django.db import models
from django.utils import timezone


class FireEquipment(models.Model):
    class Kind(models.TextChoices):
        EXTINGUISHER = "extinguisher", "Fire extinguisher"
        HOSE_REEL = "hose_reel", "Hose reel"
        ALARM = "alarm", "Fire alarm"
        SPRINKLER = "sprinkler", "Sprinkler"
        HYDRANT = "hydrant", "Hydrant"

    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="fire_equipment")
    site = models.ForeignKey("organizations.Site", on_delete=models.SET_NULL, null=True, blank=True)
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.EXTINGUISHER)
    tag_number = models.CharField(max_length=50, unique=True, help_text="e.g. EXT-IA-012")
    location_detail = models.CharField(max_length=255, blank=True)
    last_serviced = models.DateField(null=True, blank=True)
    next_service_due = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["tag_number"]

    def __str__(self):
        return self.tag_number

    @property
    def is_overdue(self):
        return bool(self.next_service_due and self.next_service_due < timezone.now().date())
