from rest_framework import serializers

from .models import PartnerPreference, ProfilePhoto, UserProfile


class ProfilePhotoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProfilePhoto
        fields = ["id", "image", "image_url", "caption", "is_primary"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if not obj.image:
            return ""
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url


class PartnerPreferenceSerializer(serializers.ModelSerializer):
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


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    location = serializers.CharField(source="current_location.city", read_only=True)
    photos = ProfilePhotoSerializer(many=True, read_only=True)
    preference = PartnerPreferenceSerializer(read_only=True)
    completion_percentage = serializers.IntegerField(read_only=True)
    biodata_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "phone",
            "age",
            "gender",
            "religion",
            "community",
            "sub_community",
            "mother_tongue",
            "gujarati_speaking",
            "location",
            "hometown",
            "about_me",
            "biodata_file",
            "biodata_url",
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
            "completion_percentage",
            "photos",
            "preference",
        ]

    def get_biodata_url(self, obj):
        request = self.context.get("request")
        if not obj.biodata_file:
            return ""
        return request.build_absolute_uri(obj.biodata_file.url) if request else obj.biodata_file.url
