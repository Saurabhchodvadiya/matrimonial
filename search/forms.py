from django import forms
from django.utils.translation import gettext_lazy as _

from locations.models import Community, Location
from profiles.models import UserProfile


class ProfileSearchForm(forms.Form):
    q = forms.CharField(required=False, label=_("Search by name/profession"))
    gender = forms.ChoiceField(required=False, choices=[("", _("Any"))] + UserProfile.GENDER_CHOICES)
    religion = forms.CharField(required=False, label=_("Religion"))
    hometown = forms.CharField(required=False, label=_("Native gam / hometown"))
    mother_tongue = forms.CharField(required=False, label=_("Mother tongue"))
    gujarati_speaking = forms.ChoiceField(
        required=False,
        label=_("Gujarati speaking"),
        choices=[("", _("Any"))] + UserProfile.GUJARATI_SPEAKING_CHOICES,
    )
    age_group = forms.ChoiceField(
        required=False,
        label=_("Age group"),
        choices=[
            ("", _("Any")),
            ("21-26", "21-26"),
            ("27-32", "27-32"),
            ("33-40", "33-40"),
        ],
    )
    community = forms.ModelChoiceField(
        required=False, queryset=Community.objects.filter(is_active=True), empty_label=_("Any community")
    )
    location = forms.ModelChoiceField(
        required=False, queryset=Location.objects.filter(is_active=True), empty_label=_("Any location")
    )
    sort = forms.ChoiceField(
        required=False,
        label=_("Sort by"),
        choices=[
            ("newest", _("Newest")),
            ("active", _("Recently active")),
            ("age_low", _("Age low to high")),
            ("age_high", _("Age high to low")),
        ],
        initial="newest",
    )
