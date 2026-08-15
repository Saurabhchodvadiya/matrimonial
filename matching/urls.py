from django.urls import path

from .views import recommended_matches_view

app_name = "matching"

urlpatterns = [
    path("", recommended_matches_view, name="recommended"),
]
