from django.urls import path

from .views import create_report_view

app_name = "reports"

urlpatterns = [
    path("create/<int:profile_id>/", create_report_view, name="create"),
]
