from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RecommendedPageTests(TestCase):
    def test_recommended_page_requires_login(self):
        response = self.client.get(reverse("matching:recommended"))
        self.assertEqual(response.status_code, 302)

    def test_logged_user_can_open_recommended_page(self):
        User.objects.create_user(username="matcher", password="Pass12345")
        self.client.login(username="matcher", password="Pass12345")
        response = self.client.get(reverse("matching:recommended"))
        self.assertEqual(response.status_code, 200)
