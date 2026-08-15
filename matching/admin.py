from django.contrib import admin
from .models import MatchRecommendation


@admin.register(MatchRecommendation)
class MatchRecommendationAdmin(admin.ModelAdmin):
    list_display = ("profile", "recommended_profile", "compatibility_score", "updated_at")
    list_filter = ("compatibility_score",)
    search_fields = ("profile__user__username", "recommended_profile__user__username")
