from django.urls import path
from . import views

app_name = "capa"

urlpatterns = [
    path("", views.ListView.as_view(), name="list"),
    path("add/", views.CreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.UpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.DeleteView.as_view(), name="delete"),
]
