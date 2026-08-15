from django.urls import path

from .views import (
    MyProfileAPIView,
    PublicProfileListAPIView,
    add_photo_view,
    delete_photo_view,
    my_profile_view,
    profile_detail_view,
    toggle_profile_active_view,
)

app_name = "profiles"

urlpatterns = [
    path("me/", my_profile_view, name="my-profile"),
    path("me/toggle-active/", toggle_profile_active_view, name="toggle-active"),
    path("me/photos/add/", add_photo_view, name="add-photo"),
    path("me/photos/<int:photo_id>/delete/", delete_photo_view, name="delete-photo"),
    path("<int:profile_id>/", profile_detail_view, name="detail"),
    path("api/list/", PublicProfileListAPIView.as_view(), name="api-list"),
    path("api/me/", MyProfileAPIView.as_view(), name="api-me"),
]
