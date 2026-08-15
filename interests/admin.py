from django.contrib import admin
from .models import Block, Interest


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("id", "from_profile", "to_profile", "status", "updated_at")
    list_filter = ("status",)
    search_fields = ("from_profile__user__username", "to_profile__user__username")


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("id", "blocker", "blocked", "created_at")
    search_fields = ("blocker__user__username", "blocked__user__username", "reason")
