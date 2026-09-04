from django.urls import path
from . import views

app_name = "toolbox"

urlpatterns = [
    path("", views.ToolboxListView.as_view(), name="list"),
    path("add/", views.ToolboxCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.ToolboxUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.ToolboxDeleteView.as_view(), name="delete"),
]
