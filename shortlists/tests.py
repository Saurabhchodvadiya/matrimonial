from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ShortlistPageTests(TestCase):
    def test_shortlist_page_requires_login(self):
        response = self.client.get(reverse("shortlists:list"))
        self.assertEqual(response.status_code, 302)

    def test_logged_user_can_open_shortlist(self):
        User.objects.create_user(username="shortuser", password="Pass12345")
        self.client.login(username="shortuser", password="Pass12345")
        response = self.client.get(reverse("shortlists:list"))
        self.assertEqual(response.status_code, 200)
