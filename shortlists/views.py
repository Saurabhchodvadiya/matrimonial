from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Shortlist


@login_required
def my_shortlist_view(request):
    shortlist_items = (
        Shortlist.objects.filter(owner=request.user.profile)
        .select_related("target__user", "target__current_location")
        .order_by("-created_at")
    )
    return render(request, "shortlists/my_shortlist.html", {"shortlist_items": shortlist_items})
