from django.urls import path

from .views import (
    block_profile_view,
    inbox_view,
    respond_interest_view,
    send_interest_view,
    toggle_shortlist_view,
    unblock_profile_view,
    withdraw_interest_view,
)

app_name = "interests"

urlpatterns = [
    path("inbox/", inbox_view, name="inbox"),
    path("send/<int:profile_id>/", send_interest_view, name="send"),
    path("respond/<int:interest_id>/<str:action>/", respond_interest_view, name="respond"),
    path("withdraw/<int:profile_id>/", withdraw_interest_view, name="withdraw"),
    path("shortlist/<int:profile_id>/", toggle_shortlist_view, name="shortlist"),
    path("block/<int:profile_id>/", block_profile_view, name="block"),
    path("unblock/<int:profile_id>/", unblock_profile_view, name="unblock"),
]
