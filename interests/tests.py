from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Block, Interest


class InterestFlowTests(TestCase):
    def setUp(self):
        self.password = "Pass12345"
        self.u1 = User.objects.create_user(username="a", password=self.password)
        self.u2 = User.objects.create_user(username="b", password=self.password)

    def test_send_interest(self):
        self.client.login(username="a", password=self.password)
        response = self.client.post(reverse("interests:send", args=[self.u2.profile.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Interest.objects.filter(from_profile=self.u1.profile, to_profile=self.u2.profile).exists()
        )

    def test_inbox_shows_profile_links_for_interests(self):
        Interest.objects.create(from_profile=self.u1.profile, to_profile=self.u2.profile)
        self.client.login(username="b", password=self.password)
        response = self.client.get(reverse("interests:inbox"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("profiles:detail", args=[self.u1.profile.id]))

    def test_unblock_removes_existing_block(self):
        Block.objects.create(blocker=self.u1.profile, blocked=self.u2.profile)
        self.client.login(username="a", password=self.password)
        response = self.client.post(reverse("interests:unblock", args=[self.u2.profile.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Block.objects.filter(blocker=self.u1.profile, blocked=self.u2.profile).exists())

    def test_inbox_shows_blocked_users_section(self):
        Block.objects.create(blocker=self.u1.profile, blocked=self.u2.profile, reason="Spam profile")
        self.client.login(username="a", password=self.password)
        response = self.client.get(reverse("interests:inbox"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blocked Users")
        self.assertContains(response, "Spam profile")
        self.assertContains(response, reverse("interests:unblock", args=[self.u2.profile.id]))
