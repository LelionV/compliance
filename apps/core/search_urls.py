from django.urls import path
from .search import global_search

app_name = "search"

urlpatterns = [
    path("", global_search, name="results"),
]
