from django.contrib import admin
from .models import Career, Education, Family, PartnerPreference, ProfilePhoto, UserProfile


class ProfilePhotoInline(admin.TabularInline):
    model = ProfilePhoto
    extra = 0


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "religion",
        "community",
        "current_location",
        "is_profile_active",
        "is_profile_hidden",
        "updated_at",
    )
    list_filter = ("religion", "is_profile_active", "is_profile_hidden", "gujarati_speaking")
    search_fields = ("user__username", "full_name", "phone", "religion", "community__name")
    inlines = [ProfilePhotoInline]


@admin.register(PartnerPreference)
class PartnerPreferenceAdmin(admin.ModelAdmin):
    list_display = ("profile", "min_age", "max_age", "preferred_religion", "preferred_community")
    search_fields = ("profile__user__username", "preferred_religion", "preferred_community")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("profile", "highest_qualification", "institution_name", "graduation_year")
    search_fields = ("profile__user__username", "highest_qualification", "institution_name")


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ("profile", "profession", "company_name", "annual_income")
    search_fields = ("profile__user__username", "profession", "company_name")


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ("profile", "family_type", "father_occupation", "mother_occupation")
    search_fields = ("profile__user__username", "family_type")
