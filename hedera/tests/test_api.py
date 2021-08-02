from vocab_list.models import PersonalVocabularyList
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
import json


class PersonalVocabularyQuickAddAPITest(APITestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(username="test_user99", email="test_user99@test.com", password="password")
        self.personal_vocab_list = PersonalVocabularyList.objects.create(user=self.created_user, lang="lat")
        self.client.force_login(user=self.created_user)

    def test_get_personal_vocabulary_quick_add_api(self):
        response = self.client.get("/api/v1/personal_vocab_list/quick_add/")
        self.assertEqual(response.status_code, 200)

    def test_post_personal_vocabulary_quick_add_api(self):
        self.client.force_login(user=self.created_user)
        payload = {
            "familiarity": 1,
            "gloss": "something",
            "headword": "ergo",
            "vocabulary_list_id": self.personal_vocab_list.id,
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
