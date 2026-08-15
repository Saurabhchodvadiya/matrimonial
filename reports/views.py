from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from profiles.models import UserProfile

from .forms import ReportForm


@login_required
def create_report_view(request, profile_id):
    reported_profile = get_object_or_404(UserProfile, id=profile_id)
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user.profile
            report.reported_profile = reported_profile
            report.save()
            messages.success(request, "Report submitted. Our team will review it.")
            return redirect("profiles:detail", profile_id=profile_id)
    else:
        form = ReportForm()
    return render(
        request, "reports/create_report.html", {"form": form, "reported_profile": reported_profile}
    )
