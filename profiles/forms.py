from django import forms

from .models import PartnerPreference, ProfilePhoto, UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "full_name",
            "phone",
            "age",
            "gender",
            "religion",
            "community",
            "sub_community",
            "mother_tongue",
            "gujarati_speaking",
            "current_location",
            "hometown",
            "about_me",
            "biodata_file",
            "highest_education",
            "education_details",
            "profession",
            "company_name",
            "annual_income",
            "family_details",
            "lifestyle",
            "is_profile_active",
            "is_profile_hidden",
            "photo_visibility",
            "show_contact_details",
        ]
        widgets = {
            "about_me": forms.Textarea(attrs={"rows": 4}),
            "education_details": forms.Textarea(attrs={"rows": 3}),
            "family_details": forms.Textarea(attrs={"rows": 3}),
            "lifestyle": forms.Textarea(attrs={"rows": 3}),
        }


class PartnerPreferenceForm(forms.ModelForm):
    class Meta:
        model = PartnerPreference
        fields = [
            "min_age",
            "max_age",
            "preferred_religion",
            "preferred_community",
            "preferred_location",
            "additional_preferences",
        ]
        widgets = {"additional_preferences": forms.Textarea(attrs={"rows": 3})}


class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = ProfilePhoto
        fields = ["image", "caption", "is_primary"]
