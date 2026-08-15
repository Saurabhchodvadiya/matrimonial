from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SuccessStory(TimeStampedModel):
    groom_name = models.CharField(max_length=120)
    bride_name = models.CharField(max_length=120)
    story = models.TextField()
    wedding_date = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.groom_name} & {self.bride_name}"
