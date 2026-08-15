from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from interests.models import Block, Interest


class ProfileAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="mehul", password="Pass12345")

    def test_my_profile_requires_auth(self):
        response = self.client.get(reverse("profiles:api-me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_my_profile_access_with_jwt(self):
        token_response = self.client.post(
            reverse("accounts:token_obtain_pair"),
            {"username": "mehul", "password": "Pass12345"},
            format="json",
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        access = token_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = self.client.get(reverse("profiles:api-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileDetailViewTests(TestCase):
    def setUp(self):
        self.password = "Pass12345"
        self.owner = User.objects.create_user(
            username="owner", email="owner@example.com", password=self.password
        )
        self.viewer = User.objects.create_user(
            username="viewer", email="viewer@example.com", password=self.password
        )
        self.owner.profile.phone = "9876543210"
        self.owner.profile.show_contact_details = False
        self.owner.profile.biodata_file.name = "profiles/biodata/sample.pdf"
        self.owner.profile.save(
            update_fields=["phone", "show_contact_details", "biodata_file", "updated_at"]
        )

    def test_profile_detail_hides_contact_without_permission(self):
        self.client.login(username="viewer", password=self.password)
        response = self.client.get(reverse("profiles:detail", args=[self.owner.profile.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, "9876543210")
        self.assertNotContains(response, "owner@example.com")

    def test_profile_detail_shows_contact_after_accepted_interest(self):
        Interest.objects.create(
            from_profile=self.viewer.profile,
            to_profile=self.owner.profile,
            status=Interest.STATUS_ACCEPTED,
        )
        self.client.login(username="viewer", password=self.password)
        response = self.client.get(reverse("profiles:detail", args=[self.owner.profile.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "9876543210")
        self.assertContains(response, "owner@example.com")

    def test_profile_detail_shows_biodata_link(self):
        self.client.login(username="viewer", password=self.password)
        response = self.client.get(reverse("profiles:detail", args=[self.owner.profile.id]))
        self.assertContains(response, "View Biodata")

    def test_profile_detail_shows_interest_sent_indicator(self):
        Interest.objects.create(
            from_profile=self.viewer.profile,
            to_profile=self.owner.profile,
            status=Interest.STATUS_PENDING,
        )
        self.client.login(username="viewer", password=self.password)
        response = self.client.get(reverse("profiles:detail", args=[self.owner.profile.id]))
        self.assertContains(response, "Interest Sent (Pending)")
        self.assertContains(response, "Withdraw Interest")

    def test_profile_detail_shows_unblock_when_already_blocked(self):
        Block.objects.create(blocker=self.viewer.profile, blocked=self.owner.profile)
        self.client.login(username="viewer", password=self.password)
        response = self.client.get(reverse("profiles:detail", args=[self.owner.profile.id]))
        self.assertContains(response, "Unblock")
        self.assertContains(response, "Profile Blocked")
