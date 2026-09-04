import io

from django.core.files.base import ContentFile
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

from apps.incidents.models import Incident
from apps.capa.models import CorrectiveAction
from apps.fire.models import FireEquipment
from apps.risk.models import RiskAssessment
from apps.doshs.models import StatutoryDeadline


def build_doshs_pack_pdf(organization) -> ContentFile:
    """Renders a DOSHS compliance pack PDF for the given organization and
    returns it as a Django ContentFile ready to attach to a FileField."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=18 * mm, bottomMargin=18 * mm, leftMargin=16 * mm, rightMargin=16 * mm,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleGreen", parent=styles["Title"], textColor=colors.HexColor("#1f7a4d"))
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], textColor=colors.HexColor("#12261e"), spaceBefore=14)
    body = styles["BodyText"]

    story = [
        Paragraph("DOSHS Compliance Pack", title_style),
        Paragraph(f"{organization.name} &mdash; {organization.dosh_reg_no or 'No DOSH reg. number on file'}", body),
        Paragraph(f"Generated {timezone.now().strftime('%d %B %Y, %H:%M')}", body),
        Spacer(1, 10 * mm),
    ]

    # Compliance score summary
    story.append(Paragraph("1. Compliance Summary", h2))
    items = organization.compliance_items.all()
    total = items.count()
    done = items.filter(is_evidenced=True).count()
    score = organization.compliance_score
    summary_data = [
        ["Statutory duties evidenced", f"{done} / {total}"],
        ["Compliance score", f"{score}%"],
        ["Registered seats", str(organization.seats)],
        ["Industry", organization.industry or "-"],
    ]
    story.append(_table(summary_data))

    # Open incidents
    story.append(Paragraph("2. Open Incidents", h2))
    incidents = Incident.objects.filter(organization=organization).exclude(status="closed")
    if incidents.exists():
        rows = [["Title", "Kind", "Severity", "Status", "Occurred"]]
        for inc in incidents[:25]:
            rows.append([inc.title, inc.get_kind_display(), inc.get_severity_display(),
                         inc.get_status_display(), inc.occurred_at.strftime("%Y-%m-%d")])
        story.append(_table(rows, header=True))
    else:
        story.append(Paragraph("No open incidents at time of generation.", body))

    # Open CAPAs
    story.append(Paragraph("3. Open Corrective Actions (CAPA)", h2))
    capas = CorrectiveAction.objects.filter(organization=organization).exclude(status="closed")
    if capas.exists():
        rows = [["Title", "Priority", "Status", "Due date"]]
        for c in capas[:25]:
            rows.append([c.title, c.get_priority_display(), c.get_status_display(), c.due_date.strftime("%Y-%m-%d")])
        story.append(_table(rows, header=True))
    else:
        story.append(Paragraph("No open corrective actions.", body))

    # Fire equipment overdue
    story.append(Paragraph("4. Fire Equipment Service Status", h2))
    fire = FireEquipment.objects.filter(organization=organization)
    overdue = [f for f in fire if f.is_overdue]
    if overdue:
        rows = [["Tag", "Kind", "Next service due"]]
        for f in overdue:
            rows.append([f.tag_number, f.get_kind_display(), f.next_service_due.strftime("%Y-%m-%d") if f.next_service_due else "-"])
        story.append(_table(rows, header=True))
    else:
        story.append(Paragraph(f"All {fire.count()} fire equipment items are within service dates.", body))

    # Risk assessments due
    story.append(Paragraph("5. Risk Assessments Due for Review", h2))
    ra_due = RiskAssessment.objects.filter(organization=organization, status="due_review")
    if ra_due.exists():
        rows = [["Activity", "Risk score", "Review date"]]
        for r in ra_due:
            rows.append([r.activity, str(r.risk_score), r.review_date.strftime("%Y-%m-%d") if r.review_date else "-"])
        story.append(_table(rows, header=True))
    else:
        story.append(Paragraph("No risk assessments currently due for review.", body))

    # Statutory deadlines
    story.append(Paragraph("6. Statutory Deadlines", h2))
    deadlines = StatutoryDeadline.objects.filter(organization=organization).exclude(status="done")
    if deadlines.exists():
        rows = [["Title", "Reference", "Due date", "Status"]]
        for d in deadlines[:25]:
            rows.append([d.title, d.statutory_reference or "-", d.due_date.strftime("%Y-%m-%d"), d.computed_status().replace("_", " ").title()])
        story.append(_table(rows, header=True))
    else:
        story.append(Paragraph("No outstanding statutory deadlines.", body))

    doc.build(story)
    buffer.seek(0)
    filename = f"doshs_pack_{organization.slug}_{timezone.now().strftime('%Y%m%d_%H%M')}.pdf"
    return ContentFile(buffer.read(), name=filename)


def _table(rows, header=False):
    t = Table(rows, hAlign="LEFT", colWidths=None)
    style = [
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e6e9e8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12261e")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    t.setStyle(TableStyle(style))
    return t
