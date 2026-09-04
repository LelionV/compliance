from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("team/", views.TeamListView.as_view(), name="team_list"),
    path("team/add/", views.TeamCreateView.as_view(), name="team_add"),
    path("team/<int:pk>/edit/", views.TeamUpdateView.as_view(), name="team_edit"),
]
