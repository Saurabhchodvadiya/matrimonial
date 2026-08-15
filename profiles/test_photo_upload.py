from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import ProfilePhoto


class ProfilePhotoUploadTests(TestCase):
    GIF_1PX = (
        b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00"
        b"\x00\x02\x02D\x01\x00;"
    )

    def test_upload_promotes_new_photo_when_primary_file_is_missing(self):
        user = User.objects.create_user(username="photo-owner", password="Pass12345")
        ProfilePhoto.objects.create(
            profile=user.profile,
            image="profiles/photos/missing-primary.jpg",
            is_primary=True,
        )

        self.client.login(username="photo-owner", password="Pass12345")
        response = self.client.post(
            reverse("profiles:add-photo"),
            {
                "image": SimpleUploadedFile(
                    "fresh.gif", self.GIF_1PX, content_type="image/gif"
                ),
                "caption": "fresh",
            },
        )

        self.assertEqual(response.status_code, 302)
        photos = list(user.profile.photos.order_by("-created_at"))
        self.assertEqual(len(photos), 2)
        self.assertTrue(photos[0].is_primary)
        self.assertFalse(photos[1].is_primary)
