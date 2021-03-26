from django.urls import path
from . import views

urlpatterns = [
    path("", views.filterView, name="filter"),
    path("api/", views.FilterListView.as_view(), name="filter_api")
]