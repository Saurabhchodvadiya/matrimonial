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
