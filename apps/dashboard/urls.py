from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("select-org/", views.SelectOrganizationView.as_view(), name="select_org"),
    path("switch-org/", views.switch_organization, name="switch_org"),
]
