from apps.core.generic import build_crud_views
from .models import CorrectiveAction

ListView, CreateView, UpdateView, DeleteView = build_crud_views(
    model=CorrectiveAction,
    fields=['source_incident', 'source_inspection', 'title', 'description', 'priority', 'status', 'due_date', 'closed_date'],
    url_namespace="capa",
    page_title="Corrective Action",
)
