import json
from random import randrange

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from lattices.models import LatticeNode
from vocab_list.models import PersonalVocabularyList


class PersonalVocabularyQuickAddAPITest(APITestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(username=f"test_user{randrange(100)}", email=f"test_user{randrange(100)}@test.com", password="password")
        self.client.force_login(user=self.created_user)
        self.personal_vocab_list = PersonalVocabularyList.objects.create(user=self.created_user, lang="lat")

    def test_fail_get_personal_vocabulary_quick_add_api(self):
        self.created_user = User.objects.create_user(username=f"test_user{randrange(100)}", email=f"test_user{randrange(100)}@test.com", password="password")
        self.client.force_login(user=self.created_user)
        response = self.client.get("/api/v1/personal_vocab_list/quick_add/")
        self.assertEqual(len(response.json()["data"]), 0)

    def test_get_personal_vocabulary_quick_add_api(self):
        response = self.client.get("/api/v1/personal_vocab_list/quick_add/")
        self.assertEqual(response.status_code, 200)

    def test_post_personal_vocabulary_quick_add_api(self):
        payload = {
            "familiarity": 1,
            "gloss": "something",
            "headword": "sum",
            "vocabulary_list_id": self.personal_vocab_list.id,
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_fail_post_personal_vocabulary_quick_add_api_missing_vocab_list_id(self):
        payload = {
            "familiarity": 1,
            "gloss": "something",
            "headword": "sum",
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_fail_post_personal_vocabulary_quick_add_api_missing_familiarity(self):
        payload = {
            "gloss": "something",
            "headword": "sum",
            "vocabulary_list_id": self.personal_vocab_list.id,
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_fail_post_personal_vocabulary_quick_add_api_missing_gloss(self):
        payload = {
            "familiarity": 1,
            "headword": "sum",
            "vocabulary_list_id": self.personal_vocab_list.id
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_fail_post_personal_vocabulary_quick_add_api_missing_headword(self):
        payload = {
            "familiarity": 1,
            "gloss": "something",
            "vocabulary_list_id": self.personal_vocab_list.id
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)


class LatticeNodesAPITest(APITestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(username=f"test_user{randrange(100)}", email=f"test_user{randrange(100)}@test.com", password="password")
        LatticeNode.objects.create(label="sum, esse, fuī", canonical=True, gloss="to be, exist")
        self.client.force_login(user=self.created_user)

    def test_get_related_lattice_nodes(self):
        response = self.client.get("/api/v1/lattice_nodes/?headword=sum")
        success_response = [
            {
                "label": "sum, esse, fuī",
                "gloss": "to be, exist",
                "canonical": True,
                "forms": [],
                "lemmas": [],
                "vocabulary_entries": [],
                "children": [],
                "parents": []
            }
        ]
        json_response = response.json()["data"]
        # delete pk because it is not constant
        del json_response[0]["pk"]
        self.assertEqual(json_response, success_response)

    def test_fail_to_get_related_lattice_nodes(self):
        response = self.client.get("/api/v1/lattice_nodes/?headword=ssss")
        self.assertEqual(len(response.json()["data"]), 0)


class MeAPITest(APITestCase):
    def setUp(self):
        self.created_user = User.objects.create_user(username=f"test_user{randrange(100)}", email=f"test_user{randrange(100)}@test.com", password="password")
        self.client.force_login(user=self.created_user)

    def test_successful_post_me_profile_with_lang_field(self):
        response = self.client.post("/api/v1/me/", json.dumps({"lang": "lat"}), content_type="application/json")
        data = response.json()["data"]
        self.assertEqual(data["lang"], "lat")

    def test_failing_post_me_profile_with_lang_field(self):
        # if language is not supported
        response = self.client.post("/api/v1/me/", json.dumps({"lang": "abc"}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
