from django.urls import path
from . import views

app_name = "doshs"

urlpatterns = [
    path("", views.ListView.as_view(), name="list"),
    path("add/", views.CreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.UpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.DeleteView.as_view(), name="delete"),
    path("generate-pack/", views.generate_pack, name="generate_pack"),
    path("calendar/", views.compliance_calendar, name="calendar"),
]
