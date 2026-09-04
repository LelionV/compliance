from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone

from apps.core.generic import build_crud_views
from .models import DOSHSReport, StatutoryDeadline
from .pdf import build_doshs_pack_pdf

ListView, CreateView, UpdateView, DeleteView = build_crud_views(
    model=DOSHSReport,
    fields=['kind', 'title', 'generated_pdf', 'submitted', 'submitted_at'],
    url_namespace="doshs",
    page_title="DOSHS Report",
)


@login_required
def generate_pack(request):
    """One-click DOSHS pack generation, as seen on the dashboard button."""
    org = request.organization
    if org is None:
        messages.error(request, "Select a company first.")
        return redirect("dashboard:select_org")

    pdf_file = build_doshs_pack_pdf(org)
    report = DOSHSReport.objects.create(
        organization=org,
        kind=DOSHSReport.Kind.DOSHS_PACK,
        title=f"DOSHS Compliance Pack — {timezone.now().strftime('%b %Y')}",
        generated_by=request.user,
        generated_at=timezone.now(),
    )
    report.generated_pdf.save(pdf_file.name, pdf_file, save=True)
    messages.success(request, "DOSHS pack generated.")
    return redirect("doshs:list")


@login_required
def compliance_calendar(request):
    """Calendar-style view of statutory deadlines, grouped by month."""
    from collections import OrderedDict
    from django.shortcuts import render

    org = request.organization
    if org is None and not request.is_all_sites:
        return redirect("dashboard:select_org")

    qs = StatutoryDeadline.objects.all() if request.is_all_sites else StatutoryDeadline.objects.filter(organization=org)
    qs = qs.order_by("due_date")

    grouped = OrderedDict()
    for d in qs:
        key = d.due_date.strftime("%B %Y")
        grouped.setdefault(key, []).append(d)

    return render(request, "doshs/calendar.html", {"grouped": grouped, "page_title": "Compliance Calendar"})
