from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render

from interests.models import Block
from profiles.models import UserProfile

from .services import calculate_compatibility_score


@login_required
def recommended_matches_view(request):
    my_profile = request.user.profile
    blocked = Block.objects.filter(blocker=my_profile, blocked=OuterRef("pk"))
    candidates = (
        UserProfile.objects.filter(is_profile_active=True, is_profile_hidden=False)
        .exclude(pk=my_profile.pk)
        .annotate(is_blocked=Exists(blocked))
        .filter(is_blocked=False)
        .select_related("community", "current_location", "user", "preference")
        .order_by("-updated_at")[:20]
    )

    cards = []
    for candidate in candidates:
        score, breakdown = calculate_compatibility_score(my_profile, candidate)
        cards.append({"profile": candidate, "score": score, "breakdown": breakdown})
    cards.sort(key=lambda item: item["score"], reverse=True)
    return render(request, "matching/recommended.html", {"cards": cards})
