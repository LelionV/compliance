from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import User
from apps.organizations.models import Organization, Site, ComplianceItem
from apps.incidents.models import Incident
from apps.risk.models import RiskAssessment
from apps.fire.models import FireEquipment
from apps.capa.models import CorrectiveAction
from apps.doshs.models import StatutoryDeadline


class Command(BaseCommand):
    help = "Seeds demo organizations, users and compliance records."

    def handle(self, *args, **options):
        today = timezone.now().date()

        # Platform admin (the auditing organization's own staff)
        if not User.objects.filter(username="auditor").exists():
            admin = User.objects.create_superuser(
                username="auditor", email="auditor@todomu.app", password="admin12345"
            )
            admin.role = User.Role.PLATFORM_ADMIN
            admin.first_name = "Toledo"
            admin.last_name = "Douglas"
            admin.job_title = "Safety & Health Officer"
            admin.save()
            self.stdout.write(self.style.SUCCESS("Created platform admin: auditor / admin12345"))

        org, _ = Organization.objects.get_or_create(
            name="Tafari Millers Ltd",
            defaults=dict(slug="tafari-millers", dosh_reg_no="DOSH/NRB/2019/64471",
                           industry="Manufacturing", seats=45),
        )
        ia = Site.objects.get_or_create(organization=org, name="Industrial Area")[0]
        thika = Site.objects.get_or_create(organization=org, name="Thika")[0]
        mombasa = Site.objects.get_or_create(organization=org, name="Mombasa")[0]

        for i in range(18):
            ComplianceItem.objects.get_or_create(
                organization=org, title=f"Statutory duty {i+1}",
                defaults={"is_evidenced": i < 14},
            )

        if not org.members.exists():
            client_user = User.objects.create_user(
                username="tafari_hse", email="hse@tafarimillers.co.ke", password="client12345",
                role=User.Role.ORG_ADMIN, organization=org,
                first_name="Grace", last_name="Wanjiru", job_title="HSE Officer",
            )
            self.stdout.write(self.style.SUCCESS("Created client user: tafari_hse / client12345"))

        # Incidents (trend data across last 6 months)
        if not Incident.objects.filter(organization=org).exists():
            for i in range(6):
                month_date = today.replace(day=10) - timedelta(days=30 * (5 - i))
                Incident.objects.create(
                    organization=org, site=ia, kind=Incident.Kind.NEAR_MISS,
                    severity=Incident.Severity.LOW, status=Incident.Status.CLOSED,
                    title=f"Near miss batch {i+1}", occurred_at=month_date,
                )
            Incident.objects.create(
                organization=org, site=thika, kind=Incident.Kind.INJURY,
                severity=Incident.Severity.MEDIUM, status=Incident.Status.AWAITING_DOSH,
                title="Forklift minor collision", occurred_at=today - timedelta(days=34),
                is_lost_time_injury=True,
            )
            Incident.objects.create(
                organization=org, site=mombasa, kind=Incident.Kind.NEAR_MISS,
                severity=Incident.Severity.LOW, status=Incident.Status.OPEN,
                title="Unmarked spill near loading bay", occurred_at=today - timedelta(days=2),
            )

        if not FireEquipment.objects.filter(organization=org).exists():
            FireEquipment.objects.create(organization=org, site=ia, tag_number="EXT-IA-012",
                                          next_service_due=today - timedelta(days=10))
            FireEquipment.objects.create(organization=org, site=mombasa, tag_number="EXT-MS-008",
                                          next_service_due=today - timedelta(days=3))
            FireEquipment.objects.create(organization=org, site=thika, tag_number="EXT-TK-004",
                                          next_service_due=today + timedelta(days=60))

        if not RiskAssessment.objects.filter(organization=org).exists():
            RiskAssessment.objects.create(organization=org, site=ia, activity="Milling line operation",
                                           status=RiskAssessment.Status.DUE_REVIEW, likelihood=3, severity=4,
                                           review_date=today - timedelta(days=1))

        if not CorrectiveAction.objects.filter(organization=org).exists():
            CorrectiveAction.objects.create(organization=org, title="Repair broken guardrail on mezzanine",
                                             priority=CorrectiveAction.Priority.HIGH,
                                             status=CorrectiveAction.Status.OVERDUE,
                                             due_date=today - timedelta(days=5))
            for i in range(4):
                CorrectiveAction.objects.create(organization=org, title=f"Open CAPA item {i+1}",
                                                 status=CorrectiveAction.Status.OPEN,
                                                 due_date=today + timedelta(days=10 + i))

        if not StatutoryDeadline.objects.filter(organization=org).exists():
            StatutoryDeadline.objects.create(organization=org, title="Fire safety audit and drill certificate",
                                              statutory_reference="Fire Risk Reduction Rules 2007",
                                              due_date=today - timedelta(days=1))
            StatutoryDeadline.objects.create(organization=org, title="Statutory examination of steam boiler & air receivers",
                                              due_date=today + timedelta(days=20))

        # A second organization to demonstrate switching
        org2, _ = Organization.objects.get_or_create(
            name="Coastal Logistics Ltd",
            defaults=dict(slug="coastal-logistics", dosh_reg_no="DOSH/MSA/2021/11029",
                           industry="Logistics", seats=22),
        )

        self.stdout.write(self.style.SUCCESS("Seed complete."))
