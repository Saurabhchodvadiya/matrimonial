from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "reporter", "reported_profile", "reason", "status", "created_at")
    list_filter = ("status", "reason")
    search_fields = (
        "reporter__user__username",
        "reported_profile__user__username",
        "details",
    )
