from django.db import models
from django.utils import timezone


class Organization(models.Model):
    """A client company whose OSH compliance is being managed/audited."""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    dosh_reg_no = models.CharField("DOSH/NRB Registration No.", max_length=100, blank=True)
    industry = models.CharField(max_length=150, blank=True)
    seats = models.PositiveIntegerField(default=10, help_text="Number of employees/seats")
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to="org_logos/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def compliance_score(self):
        """% of statutory duties evidenced. Uses ComplianceItem completion."""
        items = self.compliance_items.all()
        total = items.count()
        if not total:
            return 0
        done = items.filter(is_evidenced=True).count()
        return round((done / total) * 100)


class Site(models.Model):
    """A physical site/branch belonging to an organization (e.g. Thika, Mombasa)."""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="sites")
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("organization", "name")

    def __str__(self):
        return f"{self.name} ({self.organization.name})"


class ComplianceItem(models.Model):
    """A statutory duty that needs to be evidenced, e.g. per OSHA 2007 s.XX."""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="compliance_items")
    title = models.CharField(max_length=255)
    statutory_reference = models.CharField(max_length=255, blank=True)
    is_evidenced = models.BooleanField(default=False)
    evidence_note = models.TextField(blank=True)
    last_reviewed = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.organization.name}"
