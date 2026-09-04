from django.urls import path
from . import views

app_name = "first_aiders"

urlpatterns = [
    path("", views.FirstAiderListView.as_view(), name="list"),
    path("add/", views.FirstAiderCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.FirstAiderUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.FirstAiderDeleteView.as_view(), name="delete"),
]
