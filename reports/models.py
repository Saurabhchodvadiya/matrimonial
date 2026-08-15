from django.db import models

from common.models import TimeStampedModel
from profiles.models import UserProfile


class Report(TimeStampedModel):
    STATUS_OPEN = "open"
    STATUS_REVIEWED = "reviewed"
    STATUS_RESOLVED = "resolved"
    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_REVIEWED, "Reviewed"),
        (STATUS_RESOLVED, "Resolved"),
    ]
    REASON_CHOICES = [
        ("fake_profile", "Fake profile"),
        ("abusive_content", "Abusive content"),
        ("wrong_information", "Wrong information"),
        ("other", "Other"),
    ]

    reporter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reports_made")
    reported_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="reports_received"
    )
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    details = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_OPEN)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report by {self.reporter} against {self.reported_profile}"
