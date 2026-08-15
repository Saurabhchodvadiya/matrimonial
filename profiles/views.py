from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from interests.models import Block, Interest

from .forms import PartnerPreferenceForm, ProfilePhotoForm, UserProfileForm
from .models import PartnerPreference, ProfilePhoto, UserProfile
from .serializers import UserProfileSerializer


@login_required
def my_profile_view(request):
    profile = request.user.profile
    preference, _ = PartnerPreference.objects.get_or_create(profile=profile)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        preference_form = PartnerPreferenceForm(request.POST, instance=preference)
        if profile_form.is_valid() and preference_form.is_valid():
            profile_form.save()
            preference_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profiles:my-profile")
    else:
        profile_form = UserProfileForm(instance=profile)
        preference_form = PartnerPreferenceForm(instance=preference)

    photo_form = ProfilePhotoForm()
    return render(
        request,
        "profiles/my_profile.html",
        {
            "profile": profile,
            "profile_form": profile_form,
            "preference_form": preference_form,
            "photo_form": photo_form,
        },
    )


@login_required
def add_photo_view(request):
    profile = request.user.profile
    if request.method != "POST":
        return redirect("profiles:my-profile")

    photo_form = ProfilePhotoForm(request.POST, request.FILES)
    if photo_form.is_valid():
        photo = photo_form.save(commit=False)
        photo.profile = profile
        existing_primary = profile.photos.filter(is_primary=True).first()
        has_valid_primary = existing_primary.has_image_file if existing_primary else False
        if photo.is_primary or not has_valid_primary:
            profile.photos.update(is_primary=False)
            photo.is_primary = True
        photo.save()
        messages.success(request, "Photo uploaded successfully.")
    else:
        messages.error(request, "Please upload a valid photo.")
    return redirect("profiles:my-profile")


@login_required
def delete_photo_view(request, photo_id):
    profile = request.user.profile
    photo = get_object_or_404(ProfilePhoto, id=photo_id, profile=profile)
    if request.method == "POST":
        photo.delete()
        messages.success(request, "Photo deleted.")
    return redirect("profiles:my-profile")


@login_required
def toggle_profile_active_view(request):
    if request.method == "POST":
        profile = request.user.profile
        profile.is_profile_active = not profile.is_profile_active
        profile.save(update_fields=["is_profile_active", "updated_at"])
        messages.success(request, "Profile status updated.")
    return redirect("profiles:my-profile")


@login_required
def profile_detail_view(request, profile_id):
    profile = get_object_or_404(
        UserProfile.objects.select_related("community", "current_location", "user"),
        id=profile_id,
        is_profile_active=True,
    )
    viewer_profile = request.user.profile
    is_blocked_by_viewer = Block.objects.filter(blocker=viewer_profile, blocked=profile).exists()
    outgoing_interest = Interest.objects.filter(
        from_profile=viewer_profile, to_profile=profile
    ).first()
    incoming_interest = Interest.objects.filter(
        from_profile=profile, to_profile=viewer_profile
    ).first()

    interest_ui = {
        "can_send": True,
        "can_withdraw": False,
        "can_review_inbox": False,
        "label": "Express Interest",
    }
    if viewer_profile.id == profile.id:
        interest_ui = {
            "can_send": False,
            "can_withdraw": False,
            "can_review_inbox": False,
            "label": "This is your profile",
        }
    elif is_blocked_by_viewer:
        interest_ui = {
            "can_send": False,
            "can_withdraw": False,
            "can_review_inbox": False,
            "label": "Profile Blocked",
        }
    elif outgoing_interest:
        if outgoing_interest.status == Interest.STATUS_PENDING:
            interest_ui = {
                "can_send": False,
                "can_withdraw": True,
                "can_review_inbox": False,
                "label": "Interest Sent (Pending)",
            }
        elif outgoing_interest.status == Interest.STATUS_ACCEPTED:
            interest_ui = {
                "can_send": False,
                "can_withdraw": False,
                "can_review_inbox": False,
                "label": "Interest Accepted",
            }
        elif outgoing_interest.status == Interest.STATUS_DECLINED:
            interest_ui = {
                "can_send": False,
                "can_withdraw": False,
                "can_review_inbox": False,
                "label": "Interest Declined",
            }
    elif incoming_interest:
        if incoming_interest.status == Interest.STATUS_PENDING:
            interest_ui = {
                "can_send": False,
                "can_withdraw": False,
                "can_review_inbox": True,
                "label": "Interest Received",
            }
        elif incoming_interest.status == Interest.STATUS_ACCEPTED:
            interest_ui = {
                "can_send": False,
                "can_withdraw": False,
                "can_review_inbox": False,
                "label": "Interest Accepted",
            }

    can_view_contact = profile.show_contact_details or profile.id == viewer_profile.id
    if not can_view_contact:
        can_view_contact = Interest.objects.filter(
            Q(from_profile=viewer_profile, to_profile=profile)
            | Q(from_profile=profile, to_profile=viewer_profile),
            status=Interest.STATUS_ACCEPTED,
        ).exists()

    return render(
        request,
        "profiles/profile_detail.html",
        {
            "profile": profile,
            "can_view_contact": can_view_contact,
            "interest_ui": interest_ui,
            "is_blocked_by_viewer": is_blocked_by_viewer,
        },
    )


class PublicProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return UserProfile.objects.filter(is_profile_active=True, is_profile_hidden=False).select_related(
            "user", "community", "current_location"
        )


class MyProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.profile
