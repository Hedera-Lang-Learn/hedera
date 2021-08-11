import json

from rest_framework.test import APITestCase

from hedera.tests import utils
from lemmatized_text.models import LemmatizedTextBookmark
from vocab_list.models import PersonalVocabularyList


class PersonalVocabularyQuickAddAPITest(APITestCase):

    def setUp(self):
        self.user = utils.create_user()
        self.personal_vocab_list = PersonalVocabularyList.objects.create(user=self.user, lang="lat")
        self.client.force_login(user=self.user)

    def test_get_personal_vocabulary_quick_add_api(self):
        response = self.client.get("/api/v1/personal_vocab_list/quick_add/")
        self.assertEqual(response.status_code, 200)

    def test_post_personal_vocabulary_quick_add_api(self):
        self.client.force_login(user=self.user)
        payload = {
            "familiarity": 1,
            "gloss": "something",
            "headword": "ergo",
            "vocabulary_list_id": self.personal_vocab_list.id,
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)


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
