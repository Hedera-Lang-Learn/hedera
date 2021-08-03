import json

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from vocab_list.models import (
    PersonalVocabularyList,
    PersonalVocabularyListEntry
)


class PersonalVocabularyQuickAddAPITest(APITestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(username="test_user99", email="test_user99@test.com", password="password")
        self.personal_vocab_list = PersonalVocabularyList.objects.create(user=self.created_user, lang="lat")
        data = {
            "familiarity": 1,
            "headword": "testers",
            "gloss": "therefore",
            "vocabulary_list_id": self.personal_vocab_list.id
        }
        self.personal_vocab_list_entry = PersonalVocabularyListEntry.objects.create(**data)
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

    def test_successful_delete_personal_vocab_entry(self):
        payload = {
            "id": self.personal_vocab_list_entry.id
        }
        response = self.client.delete("/api/v1/personal_vocab_list/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_delete_personal_vocab_entry_empty_request_body(self):
        response = self.client.delete("/api/v1/personal_vocab_list/", json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_unsuccessful_delete_personal_vocab_entry_id_does_not_exist(self):
        payload = {
            "id": 9999
        }
        response = self.client.delete("/api/v1/personal_vocab_list/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 404)
