from django.contrib import admin
from .models import SuccessStory


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ("groom_name", "bride_name", "wedding_date", "is_published")
    list_filter = ("is_published",)
    search_fields = ("groom_name", "bride_name", "story")
