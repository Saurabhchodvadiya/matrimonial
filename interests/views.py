from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from profiles.models import UserProfile
from shortlists.models import Shortlist

from .models import Block, Interest


@login_required
def send_interest_view(request, profile_id):
    if request.method != "POST":
        return redirect("search:browse")

    my_profile = request.user.profile
    target = get_object_or_404(UserProfile, id=profile_id, is_profile_active=True)
    if my_profile.id == target.id:
        messages.error(request, "You cannot send interest to your own profile.")
        return redirect("profiles:detail", profile_id=profile_id)

    if Block.objects.filter(blocker=target, blocked=my_profile).exists():
        messages.error(request, "You cannot send interest to this profile.")
        return redirect("profiles:detail", profile_id=profile_id)

    interest, created = Interest.objects.get_or_create(from_profile=my_profile, to_profile=target)
    if not created and interest.status == Interest.STATUS_WITHDRAWN:
        interest.status = Interest.STATUS_PENDING
        interest.save(update_fields=["status", "updated_at"])
    messages.success(request, "Interest sent.")
    return redirect("profiles:detail", profile_id=profile_id)


@login_required
def respond_interest_view(request, interest_id, action):
    if request.method != "POST":
        return redirect("search:browse")

    interest = get_object_or_404(
        Interest, id=interest_id, to_profile=request.user.profile, status=Interest.STATUS_PENDING
    )
    if action == "accept":
        interest.status = Interest.STATUS_ACCEPTED
    elif action == "decline":
        interest.status = Interest.STATUS_DECLINED
    else:
        messages.error(request, "Invalid interest action.")
        return redirect("interests:inbox")
    interest.save(update_fields=["status", "updated_at"])
    messages.success(request, f"Interest {action}ed.")
    return redirect("interests:inbox")


@login_required
def withdraw_interest_view(request, profile_id):
    if request.method != "POST":
        return redirect("search:browse")
    interest = get_object_or_404(
        Interest, from_profile=request.user.profile, to_profile_id=profile_id
    )
    interest.status = Interest.STATUS_WITHDRAWN
    interest.save(update_fields=["status", "updated_at"])
    messages.success(request, "Interest withdrawn.")
    return redirect("profiles:detail", profile_id=profile_id)


@login_required
def toggle_shortlist_view(request, profile_id):
    if request.method != "POST":
        return redirect("search:browse")

    owner = request.user.profile
    target = get_object_or_404(UserProfile, id=profile_id, is_profile_active=True)
    if owner.id == target.id:
        messages.error(request, "You cannot shortlist your own profile.")
        return redirect("profiles:detail", profile_id=profile_id)
    shortlist, created = Shortlist.objects.get_or_create(owner=owner, target=target)
    if not created:
        shortlist.delete()
        messages.success(request, "Removed from shortlist.")
    else:
        messages.success(request, "Added to shortlist.")
    return redirect("profiles:detail", profile_id=profile_id)


@login_required
def block_profile_view(request, profile_id):
    if request.method != "POST":
        return redirect("search:browse")
    blocker = request.user.profile
    target = get_object_or_404(UserProfile, id=profile_id)
    if blocker.id == target.id:
        messages.error(request, "You cannot block your own profile.")
        return redirect("profiles:detail", profile_id=profile_id)
    Block.objects.get_or_create(
        blocker=blocker, blocked=target, defaults={"reason": request.POST.get("reason", "")}
    )
    messages.success(request, "Profile blocked.")
    return redirect("profiles:detail", profile_id=profile_id)


@login_required
def unblock_profile_view(request, profile_id):
    if request.method != "POST":
        return redirect("search:browse")
    blocker = request.user.profile
    target = get_object_or_404(UserProfile, id=profile_id)
    deleted_count, _ = Block.objects.filter(blocker=blocker, blocked=target).delete()
    if deleted_count:
        messages.success(request, "Profile unblocked.")
    else:
        messages.info(request, "This profile is not blocked.")
    return redirect("profiles:detail", profile_id=profile_id)


@login_required
def inbox_view(request):
    profile = request.user.profile
    received = profile.received_interests.select_related("from_profile__user")
    sent = profile.sent_interests.select_related("to_profile__user")
    shortlist = profile.shortlist_items.select_related("target__user")
    blocked_users = profile.blocks_made.select_related("blocked__user")
    return render(
        request,
        "interests/inbox.html",
        {
            "received": received,
            "sent": sent,
            "shortlist": shortlist,
            "blocked_users": blocked_users,
        },
    )
