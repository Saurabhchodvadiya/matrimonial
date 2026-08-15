from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import TimeStampedModel
from locations.models import Community, Location


class UserProfile(TimeStampedModel):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    GUJARATI_SPEAKING_CHOICES = [
        ("yes", "Yes"),
        ("basic", "Basic"),
        ("fluent", "Fluent"),
        ("no", "No"),
    ]
    PHOTO_VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("interest_only", "Visible after interest"),
        ("private", "Private"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    religion = models.CharField(max_length=120, blank=True)
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True)
    sub_community = models.CharField(max_length=120, blank=True)
    mother_tongue = models.CharField(max_length=120, default="Gujarati", blank=True)
    gujarati_speaking = models.CharField(
        max_length=10, choices=GUJARATI_SPEAKING_CHOICES, default="yes"
    )

    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    hometown = models.CharField(max_length=120, blank=True)
    about_me = models.TextField(blank=True)
    biodata_file = models.FileField(
        upload_to="profiles/biodata/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])],
    )

    highest_education = models.CharField(max_length=160, blank=True)
    education_details = models.TextField(blank=True)
    profession = models.CharField(max_length=160, blank=True)
    company_name = models.CharField(max_length=160, blank=True)
    annual_income = models.CharField(max_length=80, blank=True)

    family_details = models.TextField(blank=True)
    lifestyle = models.TextField(blank=True)

    is_profile_active = models.BooleanField(default=True)
    is_profile_hidden = models.BooleanField(default=False)
    photo_visibility = models.CharField(
        max_length=15, choices=PHOTO_VISIBILITY_CHOICES, default="public"
    )
    show_contact_details = models.BooleanField(default=False)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["is_profile_active", "is_profile_hidden"]),
            models.Index(fields=["religion"]),
            models.Index(fields=["gender", "age"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self):
        return self.full_name or self.user.username

    @property
    def completion_percentage(self):
        fields = [
            self.full_name,
            self.phone,
            self.age,
            self.gender,
            self.religion,
            self.mother_tongue,
            self.gujarati_speaking,
            self.current_location_id,
            self.about_me,
            self.highest_education,
            self.profession,
            self.family_details,
            self.lifestyle,
        ]
        filled = sum(1 for value in fields if value)
        return int((filled / len(fields)) * 100)

    @property
    def primary_photo(self):
        for photo in self.photos.all():
            if photo.has_image_file:
                return photo
        return None


class ProfilePhoto(TimeStampedModel):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="profiles/photos/")
    caption = models.CharField(max_length=160, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["-is_primary", "-created_at"]
        indexes = [models.Index(fields=["profile", "is_primary", "created_at"])]

    def __str__(self):
        return f"Photo for {self.profile}"

    @property
    def has_image_file(self):
        if not self.image:
            return False
        return self.image.storage.exists(self.image.name)


class PartnerPreference(TimeStampedModel):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="preference")
    min_age = models.PositiveSmallIntegerField(default=21)
    max_age = models.PositiveSmallIntegerField(default=35)
    preferred_religion = models.CharField(max_length=120, blank=True)
    preferred_community = models.CharField(max_length=120, blank=True)
    preferred_location = models.CharField(max_length=120, blank=True)
    additional_preferences = models.TextField(blank=True)

    def clean(self):
        if self.min_age > self.max_age:
            raise ValidationError("Minimum age cannot be greater than maximum age.")

    def __str__(self):
        return f"Preference for {self.profile}"


class Education(TimeStampedModel):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="education")
    highest_qualification = models.CharField(max_length=160, blank=True)
    institution_name = models.CharField(max_length=200, blank=True)
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True)
    education_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Education of {self.profile}"


class Career(TimeStampedModel):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="career")
    profession = models.CharField(max_length=160, blank=True)
    company_name = models.CharField(max_length=160, blank=True)
    annual_income = models.CharField(max_length=80, blank=True)
    work_location = models.CharField(max_length=120, blank=True)
    career_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Career of {self.profile}"


class Family(TimeStampedModel):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="family")
    family_type = models.CharField(max_length=120, blank=True)
    father_occupation = models.CharField(max_length=160, blank=True)
    mother_occupation = models.CharField(max_length=160, blank=True)
    siblings = models.CharField(max_length=120, blank=True)
    family_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Family of {self.profile}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance, full_name=instance.username)
        PartnerPreference.objects.create(profile=profile)
        Education.objects.create(profile=profile)
        Career.objects.create(profile=profile)
        Family.objects.create(profile=profile)
