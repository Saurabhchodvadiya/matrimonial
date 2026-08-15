from django.contrib import admin
from .models import Community, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "country", "is_active")
    list_filter = ("state", "country", "is_active")
    search_fields = ("city", "state", "country")


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
