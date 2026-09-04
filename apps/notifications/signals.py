from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.incidents.models import Incident
from apps.capa.models import CorrectiveAction
from apps.doshs.models import DOSHSReport
from .models import Notification


@receiver(post_save, sender=Incident)
def notify_new_incident(sender, instance, created, **kwargs):
    if not created:
        return
    level = Notification.Level.DANGER if instance.severity in ("high", "critical") else Notification.Level.WARNING
    Notification.notify_organization(
        instance.organization,
        f"New {instance.get_kind_display().lower()} reported: {instance.title}",
        level=level,
        link="/incidents/",
    )


@receiver(post_save, sender=CorrectiveAction)
def notify_capa(sender, instance, created, **kwargs):
    if created:
        Notification.notify_organization(
            instance.organization,
            f"New CAPA raised: {instance.title}",
            level=Notification.Level.INFO,
            link="/capa/",
        )
    elif instance.status == CorrectiveAction.Status.OVERDUE:
        Notification.notify_organization(
            instance.organization,
            f"CAPA overdue: {instance.title}",
            level=Notification.Level.DANGER,
            link="/capa/",
        )


@receiver(post_save, sender=DOSHSReport)
def notify_report_generated(sender, instance, created, **kwargs):
    if created:
        Notification.notify_organization(
            instance.organization,
            f"DOSHS report generated: {instance.title}",
            level=Notification.Level.INFO,
            link="/doshs-reports/",
        )
