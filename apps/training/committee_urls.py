from django.urls import path
from . import views

app_name = "committee"

urlpatterns = [
    path("", views.CommitteeListView.as_view(), name="list"),
    path("add/", views.CommitteeCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.CommitteeUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.CommitteeDeleteView.as_view(), name="delete"),
]
