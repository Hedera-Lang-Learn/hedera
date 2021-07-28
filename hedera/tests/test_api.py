import json
from random import randrange

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from lattices.models import LatticeNode
from vocab_list.models import PersonalVocabularyList


class PersonalVocabularyQuickAddAPITest(APITestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(username=f"test_user{randrange(100)}", email=f"test_user{randrange(100)}@test.com", password="password")
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
            "headword": "sum",
            "vocabulary_list_id": self.personal_vocab_list.id,
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)


class LatticeNodesAPITest(APITestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(username=f"test_user{randrange(100)}", email=f"test_user{randrange(100)}@test.com", password="password")
        LatticeNode.objects.create(label="sum, esse, fuī", canonical=True, gloss="to be, exist")

    def test_get_related_lattice_nodes(self):
        self.client.force_login(user=self.created_user)
        response = self.client.get("/api/v1/lattice_nodes/?headword=sum")
        success_response = [
            {
                "pk": 1,
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
        self.assertEqual(response.json()["data"], success_response)


class MeAPITest(APITestCase):
    def setUp(self):
        self.created_user = User.objects.create_user(username=f"test_user{randrange(100)}", email=f"test_user{randrange(100)}@test.com", password="password")

    def test_post_me_profile_with_lang_field(self):

        self.client.force_login(user=self.created_user)
        response = self.client.post("/api/v1/me/", json.dumps({"lang": "lat"}), content_type="application/json")
        data = response.json()["data"]
        self.assertEqual(data["lang"], "lat")
