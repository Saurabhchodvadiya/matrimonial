from django.db import models
from django.db.models import Q

from common.models import TimeStampedModel
from profiles.models import UserProfile


class Interest(TimeStampedModel):
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_DECLINED = "declined"
    STATUS_WITHDRAWN = "withdrawn"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_DECLINED, "Declined"),
        (STATUS_WITHDRAWN, "Withdrawn"),
    ]

    from_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="sent_interests"
    )
    to_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="received_interests"
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["from_profile", "to_profile"], name="unique_interest_pair"),
            models.CheckConstraint(
                condition=~Q(from_profile=models.F("to_profile")), name="no_self_interest"
            ),
        ]
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["to_profile", "status", "updated_at"]),
            models.Index(fields=["from_profile", "status", "updated_at"]),
        ]

    def __str__(self):
        return f"{self.from_profile} -> {self.to_profile} ({self.status})"


class Block(TimeStampedModel):
    blocker = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="blocks_made")
    blocked = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="blocks_received")
    reason = models.CharField(max_length=200, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["blocker", "blocked"], name="unique_block_pair"),
            models.CheckConstraint(condition=~Q(blocker=models.F("blocked")), name="no_self_block"),
        ]
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["blocker", "created_at"])]

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"
