from apps.core.generic import build_crud_views
from .models import Incident

ListView, CreateView, UpdateView, DeleteView = build_crud_views(
    model=Incident,
    fields=['site', 'kind', 'severity', 'status', 'title', 'description', 'location_detail', 'occurred_at', 'is_lost_time_injury', 'dosh_filed'],
    url_namespace="incidents",
    page_title="Incident",
)
