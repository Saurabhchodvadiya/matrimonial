from django.contrib import admin
from .models import Shortlist


@admin.register(Shortlist)
class ShortlistAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "target", "created_at")
    search_fields = ("owner__user__username", "target__user__username")
    list_filter = ("created_at",)
