from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class SearchFilterTests(TestCase):
    def setUp(self):
        self.password = "Pass12345"
        self.viewer = User.objects.create_user(username="viewer", password=self.password)
        self.match_user = User.objects.create_user(username="match", password=self.password)
        self.other_user = User.objects.create_user(username="other", password=self.password)

        self.match_user.profile.full_name = "Gujarati Match"
        self.match_user.profile.gender = "female"
        self.match_user.profile.age = 25
        self.match_user.profile.hometown = "Surat"
        self.match_user.profile.mother_tongue = "Gujarati"
        self.match_user.profile.gujarati_speaking = "fluent"
        self.match_user.profile.save()

        self.other_user.profile.full_name = "Other Match"
        self.other_user.profile.gender = "male"
        self.other_user.profile.age = 35
        self.other_user.profile.hometown = "Delhi"
        self.other_user.profile.mother_tongue = "Hindi"
        self.other_user.profile.gujarati_speaking = "no"
        self.other_user.profile.save()

    def test_search_filters_by_gujarati_fields(self):
        self.client.login(username="viewer", password=self.password)
        response = self.client.get(
            reverse("search:browse"),
            {
                "gender": "female",
                "hometown": "Surat",
                "mother_tongue": "Gujarati",
                "gujarati_speaking": "fluent",
                "age_group": "21-26",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gujarati Match")
        self.assertNotContains(response, "Other Match")
