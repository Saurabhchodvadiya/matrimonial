from django.db import models

from common.models import TimeStampedModel


class Location(TimeStampedModel):
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, default="Gujarat")
    country = models.CharField(max_length=120, default="India")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("city", "state", "country")
        ordering = ["city"]
        indexes = [
            models.Index(fields=["country", "state", "city"]),
            models.Index(fields=["is_active", "city"]),
        ]

    def __str__(self):
        return f"{self.city}, {self.state}"


class Community(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["is_active", "name"])]

    def __str__(self):
        return self.name
