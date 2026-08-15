from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from interests.models import Block
from profiles.models import UserProfile

from .forms import ProfileSearchForm


@login_required
def browse_profiles_view(request):
    my_profile = request.user.profile
    blocked_ids = Block.objects.filter(blocker=my_profile).values_list("blocked_id", flat=True)

    queryset = UserProfile.objects.filter(is_profile_active=True, is_profile_hidden=False).exclude(
        id__in=blocked_ids
    )
    queryset = queryset.select_related("community", "current_location", "user")

    form = ProfileSearchForm(request.GET or None)
    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            queryset = queryset.filter(
                Q(full_name__icontains=q) | Q(profession__icontains=q) | Q(about_me__icontains=q)
            )
        gender = form.cleaned_data.get("gender")
        if gender:
            queryset = queryset.filter(gender=gender)
        religion = form.cleaned_data.get("religion")
        if religion:
            queryset = queryset.filter(religion__icontains=religion)
        hometown = form.cleaned_data.get("hometown")
        if hometown:
            queryset = queryset.filter(hometown__icontains=hometown)
        mother_tongue = form.cleaned_data.get("mother_tongue")
        if mother_tongue:
            queryset = queryset.filter(mother_tongue__icontains=mother_tongue)
        gujarati_speaking = form.cleaned_data.get("gujarati_speaking")
        if gujarati_speaking:
            queryset = queryset.filter(gujarati_speaking=gujarati_speaking)
        age_group = form.cleaned_data.get("age_group")
        if age_group == "21-26":
            queryset = queryset.filter(age__gte=21, age__lte=26)
        elif age_group == "27-32":
            queryset = queryset.filter(age__gte=27, age__lte=32)
        elif age_group == "33-40":
            queryset = queryset.filter(age__gte=33, age__lte=40)
        community = form.cleaned_data.get("community")
        if community:
            queryset = queryset.filter(community=community)
        location = form.cleaned_data.get("location")
        if location:
            queryset = queryset.filter(current_location=location)

        sort = form.cleaned_data.get("sort") or "newest"
        if sort == "active":
            queryset = queryset.order_by("-updated_at")
        elif sort == "age_low":
            queryset = queryset.order_by("age", "-updated_at")
        elif sort == "age_high":
            queryset = queryset.order_by("-age", "-updated_at")
        else:
            queryset = queryset.order_by("-created_at")

    queryset = queryset.exclude(id=my_profile.id)
    return render(request, "search/browse.html", {"form": form, "profiles": queryset[:50]})
