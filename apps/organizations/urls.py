from django.urls import path
from . import views

app_name = "organizations"

urlpatterns = [
    path("", views.OrganizationListView.as_view(), name="list"),
    path("add/", views.OrganizationCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", views.OrganizationUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.OrganizationDeleteView.as_view(), name="delete"),
    path("<int:org_pk>/sites/add/", views.SiteCreateView.as_view(), name="site_add"),
    path("<int:org_pk>/sites/<int:pk>/delete/", views.SiteDeleteView.as_view(), name="site_delete"),
]
