from django.db import models
from django.db.models import Q

from common.models import TimeStampedModel
from profiles.models import UserProfile


class Shortlist(TimeStampedModel):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="shortlist_items")
    target = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="shortlisted_by")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "target"], name="unique_shortlist_pair"),
            models.CheckConstraint(condition=~Q(owner=models.F("target")), name="no_self_shortlist"),
        ]
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["owner", "created_at"])]

    def __str__(self):
        return f"{self.owner} shortlisted {self.target}"
