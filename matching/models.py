from django.db import models

from common.models import TimeStampedModel
from profiles.models import UserProfile


class MatchRecommendation(TimeStampedModel):
    profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="recommendations_for_me"
    )
    recommended_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="recommended_to_others"
    )
    compatibility_score = models.PositiveSmallIntegerField(default=0)
    score_breakdown = models.JSONField(default=dict, blank=True)
    rationale = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "recommended_profile"], name="unique_profile_recommendation"
            ),
            models.CheckConstraint(
                condition=~models.Q(profile=models.F("recommended_profile")),
                name="no_self_recommendation",
            ),
        ]
        ordering = ["-compatibility_score", "-updated_at"]
        indexes = [
            models.Index(fields=["profile", "compatibility_score"]),
            models.Index(fields=["recommended_profile"]),
        ]

    def __str__(self):
        return f"{self.profile} -> {self.recommended_profile} ({self.compatibility_score}%)"
