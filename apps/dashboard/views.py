from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView

from apps.core.middleware import SESSION_KEY
from apps.core.mixins import PlatformAdminRequiredMixin
from apps.organizations.models import Organization
from apps.incidents.models import Incident
from apps.capa.models import CorrectiveAction
from apps.doshs.models import StatutoryDeadline
from apps.fire.models import FireEquipment
from apps.risk.models import RiskAssessment
from apps.organizations.models import Site


class SelectOrganizationView(PlatformAdminRequiredMixin, ListView):
    """Platform admins land here if they haven't chosen a company yet."""
    model = Organization
    template_name = "dashboard/select_org.html"
    context_object_name = "organizations"
    queryset = Organization.objects.filter(is_active=True).order_by("name")


@login_required
def switch_organization(request):
    if not request.user.is_platform_admin:
        messages.error(request, "You are not permitted to switch organizations.")
        return redirect("dashboard:home")

    org_id = request.POST.get("organization_id") or request.GET.get("organization_id")
    if org_id == "ALL":
        request.session[SESSION_KEY] = "ALL"
        messages.success(request, "Now viewing all sites.")
    else:
        org = Organization.objects.filter(pk=org_id, is_active=True).first()
        if org:
            request.session[SESSION_KEY] = org.pk
            messages.success(request, f"Switched to {org.name}.")
        else:
            messages.error(request, "Organization not found.")
    return redirect(request.POST.get("next") or reverse("dashboard:home"))


class HomeView(LoginRequiredMixin, TemplateView):
    """The Safety Command Centre — mirrors the reference dashboard."""
    template_name = "dashboard/home.html"

    def get(self, request, *args, **kwargs):
        if request.organization is None and not request.is_all_sites:
            return redirect("dashboard:select_org")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        request = self.request
        today = timezone.now().date()

        if request.is_all_sites:
            incident_qs = Incident.objects.all()
            capa_qs = CorrectiveAction.objects.all()
            deadline_qs = StatutoryDeadline.objects.all()
            fire_qs = FireEquipment.objects.all()
            risk_qs = RiskAssessment.objects.all()
            org = None
        else:
            org = request.organization
            incident_qs = Incident.objects.filter(organization=org)
            capa_qs = CorrectiveAction.objects.filter(organization=org)
            deadline_qs = StatutoryDeadline.objects.filter(organization=org)
            fire_qs = FireEquipment.objects.filter(organization=org)
            risk_qs = RiskAssessment.objects.filter(organization=org)

        open_incidents = incident_qs.exclude(status="closed")
        open_capas = capa_qs.exclude(status="closed")

        last_lti = incident_qs.filter(is_lost_time_injury=True).order_by("-occurred_at").first()
        days_since_lti = (today - last_lti.occurred_at.date()).days if last_lti else None

        overdue_fire = fire_qs.filter(next_service_due__lt=today)
        due_soon_deadlines = [d for d in deadline_qs if d.computed_status() in ("overdue", "due_soon")][:6]

        # near-miss / injury trend, last 6 months
        month_labels = []
        near_miss_series = []
        injury_series = []
        cursor = today.replace(day=1)
        buckets = []
        for i in range(5, -1, -1):
            year = cursor.year
            month = cursor.month - i
            while month <= 0:
                month += 12
                year -= 1
            buckets.append((year, month))
        for (year, month) in buckets:
            month_labels.append(f"{year}-{month:02d}")
            near_miss_series.append(
                incident_qs.filter(kind="near_miss", occurred_at__year=year, occurred_at__month=month).count()
            )
            injury_series.append(
                incident_qs.filter(kind="injury", occurred_at__year=year, occurred_at__month=month).count()
            )

        # Compliance by site — % of inspections completed per site (evidence completeness)
        site_labels, site_scores = [], []
        sites_qs = Site.objects.filter(organization=org) if org else Site.objects.all()
        for site in sites_qs:
            from apps.inspections.models import Inspection
            site_inspections = Inspection.objects.filter(site=site)
            total = site_inspections.count()
            completed = site_inspections.filter(status="completed").count()
            score = round((completed / total) * 100) if total else 100
            site_labels.append(site.name)
            site_scores.append(score)

        ctx.update({
            "org": org,
            "compliance_score": org.compliance_score if org else None,
            "open_incidents_count": open_incidents.count(),
            "open_incidents_awaiting_dosh": open_incidents.filter(status="awaiting_dosh").count(),
            "open_capas_count": open_capas.count(),
            "overdue_capas_count": capa_qs.filter(status="overdue").count(),
            "days_since_lti": days_since_lti,
            "overdue_fire_equipment": overdue_fire,
            "due_soon_deadlines": due_soon_deadlines,
            "risk_assessments_due": risk_qs.filter(status="due_review").count(),
            "month_labels": month_labels,
            "near_miss_series": near_miss_series,
            "injury_series": injury_series,
            "site_labels": site_labels,
            "site_scores": site_scores,
        })
        return ctx
