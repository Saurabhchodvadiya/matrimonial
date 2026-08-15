from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthAPITests(APITestCase):
    def test_register_creates_user_and_jwt_login_works(self):
        payload = {
            "username": "harsh",
            "email": "harsh@example.com",
            "password": "SafePass123",
            "password_confirm": "SafePass123",
        }
        response = self.client.post(reverse("accounts:api-register"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        token_response = self.client.post(
            reverse("accounts:token_obtain_pair"),
            {"username": "harsh", "password": "SafePass123"},
            format="json",
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", token_response.data)


class LogoutTests(TestCase):
    def test_logout_clears_authenticated_session_and_redirects_home(self):
        user = get_user_model().objects.create_user(
            username="mehul",
            email="mehul@example.com",
            password="SafePass123",
        )
        self.client.force_login(user)
        session = self.client.session
        session["demo_key"] = "demo"
        session.save()

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("home"))
        self.assertEqual(
            response.headers.get("Cache-Control"),
            "no-cache, no-store, must-revalidate, private",
        )
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertNotIn("demo_key", self.client.session)

    def test_authenticated_page_disables_browser_caching(self):
        user = get_user_model().objects.create_user(
            username="darshan",
            email="darshan@example.com",
            password="SafePass123",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("search:browse"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.headers.get("Cache-Control"),
            "no-cache, no-store, must-revalidate, private",
        )
        self.assertEqual(response.headers.get("Pragma"), "no-cache")
        self.assertEqual(response.headers.get("Expires"), "0")
