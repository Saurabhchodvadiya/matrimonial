from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from profiles.models import ProfilePhoto


class SearchMediaUrlTests(TestCase):
    def test_search_profile_photo_uses_absolute_media_url(self):
        viewer = User.objects.create_user(username="viewer-media", password="Pass12345")
        match_user = User.objects.create_user(username="match-media", password="Pass12345")
        match_user.profile.full_name = "Photo Match"
        match_user.profile.save(update_fields=["full_name", "updated_at"])
        ProfilePhoto.objects.create(
            profile=match_user.profile,
            image="profiles/photos/test.jpg",
            is_primary=True,
        )

        self.client.login(username=viewer.username, password="Pass12345")
        response = self.client.get(reverse("search:browse"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'src="/media/profiles/photos/test.jpg"')
