from django.urls import path

from .views import my_shortlist_view

app_name = "shortlists"

urlpatterns = [
    path("", my_shortlist_view, name="list"),
]
