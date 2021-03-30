from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("", views.filterView, name="filter"),
    path("api/", views.FilterListView.as_view(), name="filter_api"),
    path("search-expenses/", csrf_exempt(views.search_result), name="search-expenses"),
]