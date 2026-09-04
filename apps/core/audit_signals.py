from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.incidents.models import Incident
from apps.risk.models import RiskAssessment
from apps.inspections.models import Inspection
from apps.capa.models import CorrectiveAction
from apps.doshs.models import DOSHSReport, StatutoryDeadline
from apps.fire.models import FireEquipment
from apps.organizations.models import ComplianceItem

from .current_user import get_current_user
from .models import AuditLogEntry

TRACKED_MODELS = [
    Incident, RiskAssessment, Inspection, CorrectiveAction,
    DOSHSReport, StatutoryDeadline, FireEquipment, ComplianceItem,
]


def _log(instance, action):
    user = get_current_user()
    org = getattr(instance, "organization", None)
    AuditLogEntry.objects.create(
        organization=org,
        actor=user if user and getattr(user, "is_authenticated", False) else None,
        action=action,
        model_label=instance._meta.label,
        object_repr=str(instance)[:255],
        object_id=str(instance.pk),
    )


def _make_save_handler():
    def handler(sender, instance, created, **kwargs):
        _log(instance, AuditLogEntry.Action.CREATE if created else AuditLogEntry.Action.UPDATE)
    return handler


def _make_delete_handler():
    def handler(sender, instance, **kwargs):
        _log(instance, AuditLogEntry.Action.DELETE)
    return handler


for model in TRACKED_MODELS:
    post_save.connect(_make_save_handler(), sender=model, weak=False)
    post_delete.connect(_make_delete_handler(), sender=model, weak=False)
