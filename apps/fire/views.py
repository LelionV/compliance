from apps.core.generic import build_crud_views
from .models import FireEquipment

ListView, CreateView, UpdateView, DeleteView = build_crud_views(
    model=FireEquipment,
    fields=['site', 'kind', 'tag_number', 'location_detail', 'last_serviced', 'next_service_due'],
    url_namespace="fire",
    page_title="Fire Equipment",
)
