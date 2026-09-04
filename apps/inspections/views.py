from apps.core.generic import build_crud_views
from .models import Inspection

ListView, CreateView, UpdateView, DeleteView = build_crud_views(
    model=Inspection,
    fields=['site', 'title', 'checklist_notes', 'status', 'scheduled_date', 'completed_date', 'signature_image'],
    url_namespace="inspections",
    page_title="Inspection",
)
