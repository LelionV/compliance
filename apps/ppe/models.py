from django.conf import settings
from django.db import models
from django.utils import timezone


class PPEItem(models.Model):
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="ppe_items")
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=5)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def low_stock(self):
        return self.stock_quantity <= self.reorder_level


class PPEIssuance(models.Model):
    organization = models.ForeignKey("organizations.Organization", on_delete=models.CASCADE, related_name="ppe_issuances")
    item = models.ForeignKey(PPEItem, on_delete=models.CASCADE, related_name="issuances")
    employee_name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField(default=1)
    issued_on = models.DateField(default=timezone.now)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    signature_image = models.ImageField(upload_to="signatures/ppe/", blank=True, null=True)

    class Meta:
        ordering = ["-issued_on"]

    def __str__(self):
        return f"{self.item} -> {self.employee_name}"
