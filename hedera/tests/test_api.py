import json
from random import randrange

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from hedera.tests import utils
from lattices.models import LatticeNode, LemmaNode
from lemmatized_text.models import LemmatizedTextBookmark
from vocab_list.models import (
    PersonalVocabularyList,
    PersonalVocabularyListEntry
)


class PersonalVocabularyQuickAddAPITest(APITestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(username=f"test_user{randrange(100)}", email=f"test_user{randrange(100)}@test.com", password="password")
        self.client.force_login(user=self.created_user)
        self.personal_vocab_list = PersonalVocabularyList.objects.create(user=self.created_user, lang="lat")
        data = {
            "familiarity": 1,
            "headword": "testers",
            "gloss": "therefore",
            "vocabulary_list_id": self.personal_vocab_list.id
        }
        self.personal_vocab_list_entry = PersonalVocabularyListEntry.objects.create(**data)

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
# Delete Test

    def test_successful_delete_personal_vocab_entry(self):
        payload = {
            "id": self.personal_vocab_list_entry.id
        }
        response = self.client.delete("/api/v1/personal_vocab_list/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_delete_personal_vocab_entry_empty_request_body(self):
        response = self.client.delete("/api/v1/personal_vocab_list/", json.dumps({}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "missing 'id'")

    def test_unsuccessful_delete_personal_vocab_entry_id_does_not_exist(self):
        payload = {
            "id": 9999
        }
        response = self.client.delete("/api/v1/personal_vocab_list/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "could not find vocab with id=9999")


class BookmarksListAPITest(APITestCase):

    def setUp(self):
        self.user = utils.create_user()
        self.client.force_login(user=self.user)
        self.texts = [utils.create_lemmatized_text(created_by=self.user) for _ in range(3)]
        self.bookmarks = [utils.create_bookmark(user=self.user, text=text) for text in self.texts]

    def test_get_bookmarks_list(self):
        response = self.client.get(f"/api/v1/bookmarks/", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        content = json.loads(response.content)
        self.assertEqual(len(self.bookmarks), len(content["data"]))

    def test_add_bookmark(self):
        new_text = utils.create_lemmatized_text(created_by=self.user)
        payload = {
            "textId": new_text.pk,
        }
        response = self.client.post(f"/api/v1/bookmarks/", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        content = json.loads(response.content)
        self.assertEqual(new_text.pk, content["data"]["text"]["id"])


class LatticeNodesAPITest(APITestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(username=f"test_user{randrange(100)}", email=f"test_user{randrange(100)}@test.com", password="password")
        self.lattice_node = LatticeNode.objects.create(label="sum, esse, fuī", canonical=True, gloss="to be, exist")
        LemmaNode.objects.create(context="morpheus", lemma="sum", node_id=self.lattice_node.pk)
        self.client.force_login(user=self.created_user)

    def test_get_related_lattice_nodes(self):
        response = self.client.get("/api/v1/lattice_nodes/?headword=sum")
        success_response = [
            {
                "pk": self.lattice_node.pk,
                "label": "sum, esse, fuī",
                "gloss": "to be, exist",
                "canonical": True,
                "forms": [],
                "lemmas": [
                    {
                        "lemma": "sum",
                        "context": "morpheus"
                    }
                ],
                "vocabulary_entries": [],
                "children": [],
                "parents": []
            }
        ]
        json_response = response.json()["data"]
        self.assertEqual(json_response[0]["pk"], success_response[0]["pk"])
        self.assertEqual(json_response[0]["label"], success_response[0]["label"])
        self.assertEqual(json_response[0]["lemmas"], success_response[0]["lemmas"])

    def test_fail_to_get_related_lattice_nodes(self):
        response = self.client.get("/api/v1/lattice_nodes/?headword=ssss")
        self.assertEqual(len(response.json()["data"]), 0)

    def test_fail_headword_not_provided(self):
        response = self.client.get("/api/v1/lattice_nodes/?headword=")
        self.assertEqual(len(response.json()["data"]), 0)

    def test_fail_headword_query_key_not_provided(self):
        response = self.client.get("/api/v1/lattice_nodes/")
        self.assertEqual(response.json()["error"], "Missing headword")


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
        self.assertEqual(response.json()["error"], "language not supported")


class BookmarksDetailAPITest(APITestCase):

    def setUp(self):
        self.user = utils.create_user()
        self.client.force_login(user=self.user)
        self.text = utils.create_lemmatized_text()
        self.bookmark = utils.create_bookmark(user=self.user, text=self.text)

    def test_get_bookmark(self):
        response = self.client.get(f"/api/v1/bookmarks/{self.bookmark.pk}/", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        expected = dict(data=dict(self.bookmark.api_data()))
        actual = json.loads(response.content)
        self.assertEqual(expected["data"].keys(), actual["data"].keys())
        self.assertEqual(expected["data"]["userId"], actual["data"]["userId"])
        self.assertEqual(expected["data"]["text"].keys(), actual["data"]["text"].keys())
        self.assertEqual(expected["data"]["text"]["id"], actual["data"]["text"]["id"])

    def test_get_bookmark_not_found_because_does_not_exist(self):
        self.bookmark.delete()
        response = self.client.get(f"/api/v1/bookmarks/{self.bookmark.pk}/", content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_get_bookmark_not_found_because_not_authorized(self):
        # change ownership of bookmark so it's not the same as the logged-in user
        self.bookmark.user = utils.create_user()
        self.bookmark.save()
        self.assertNotEqual(self.bookmark.user.pk, self.user.pk)

        response = self.client.get(f"/api/v1/bookmarks/{self.bookmark.pk}/", content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_bookmark(self):
        response = self.client.delete(f"/api/v1/bookmarks/{self.bookmark.pk}/", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual("{}", response.content.decode())

        with self.assertRaises(LemmatizedTextBookmark.DoesNotExist):
            LemmatizedTextBookmark.objects.get(pk=self.bookmark.pk)
