from django.urls import path
from . import views

app_name = "jsa"

urlpatterns = [
    path("", views.JSAListView.as_view(), name="list"),
    path("add/", views.JSACreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.JSAUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.JSADeleteView.as_view(), name="delete"),
]
