from apps.core.generic import build_crud_views
from .models import PPEItem

ListView, CreateView, UpdateView, DeleteView = build_crud_views(
    model=PPEItem,
    fields=['name', 'category', 'stock_quantity', 'reorder_level'],
    url_namespace="ppe",
    page_title="PPE Item",
)
