from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
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
            image=SimpleUploadedFile("test.jpg", b"test-image-bytes", content_type="image/jpeg"),
            is_primary=True,
        )

        self.client.login(username=viewer.username, password="Pass12345")
        response = self.client.get(reverse("search:browse"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'src="/media/profiles/photos/test')

    def test_search_ignores_primary_photo_when_file_missing(self):
        viewer = User.objects.create_user(username="viewer-media2", password="Pass12345")
        match_user = User.objects.create_user(username="match-media2", password="Pass12345")
        match_user.profile.full_name = "Photo Fallback Match"
        match_user.profile.save(update_fields=["full_name", "updated_at"])

        ProfilePhoto.objects.create(
            profile=match_user.profile,
            image="profiles/photos/missing-file.jpg",
            is_primary=True,
        )
        ProfilePhoto.objects.create(
            profile=match_user.profile,
            image=SimpleUploadedFile("valid.jpg", b"valid-image-bytes", content_type="image/jpeg"),
            is_primary=False,
        )

        self.client.login(username=viewer.username, password="Pass12345")
        response = self.client.get(reverse("search:browse"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Photo Fallback Match")
        self.assertContains(response, 'src="/media/profiles/photos/valid')
