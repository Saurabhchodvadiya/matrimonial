from django.urls import path

from .views import browse_profiles_view

app_name = "search"

urlpatterns = [
    path("", browse_profiles_view, name="browse"),
]
