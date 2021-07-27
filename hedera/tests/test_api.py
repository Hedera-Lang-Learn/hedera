import json

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from lemmatized_text.models import LemmatizedText, LemmatizedTextBookmark
from vocab_list.models import PersonalVocabularyList


TEST_USER = dict(
    username="test_user99",
    email="test_user99@test.com",
    password="not_a_real_password",
)


class PersonalVocabularyQuickAddAPITest(APITestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(**TEST_USER)
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
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)


class BookmarksListAPITest(APITestCase):
    pass


class BookmarksDetailAPITest(APITestCase):

    def setUp(self):
        self.created_user = User.objects.create_user(**TEST_USER)
        self.client.force_login(user=self.created_user)

        self.text = LemmatizedText.objects.create(
            title="C. Julius Caesar, De bello Gallico - Section 1",
            lang="lat",
            original_text="Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur.",
            created_by=self.created_user,
            public=False,
            completed=100,
            data=[],
        )

    def test_get_bookmark(self):
        bookmark, _ = LemmatizedTextBookmark.objects.get_or_create(
            user=self.created_user,
            text=self.text,
        )
        response = self.client.get(f"/api/v1/bookmarks/{bookmark.pk}/", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        expected = dict(data=dict(bookmark=bookmark.api_data()))
        actual = json.loads(response.content)

        self.assertEqual(expected["data"]["bookmark"].keys(), actual["data"]["bookmark"].keys())
        self.assertEqual(expected["data"]["bookmark"]["userId"], actual["data"]["bookmark"]["userId"])
        self.assertEqual(expected["data"]["bookmark"]["text"].keys(), actual["data"]["bookmark"]["text"].keys())
        self.assertEqual(expected["data"]["bookmark"]["text"]["id"], actual["data"]["bookmark"]["text"]["id"])

    def test_delete_bookmark(self):
        bookmark, _ = LemmatizedTextBookmark.objects.get_or_create(
            user=self.created_user,
            text=self.text,
        )
        response = self.client.delete(f"/api/v1/bookmarks/{bookmark.pk}/", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual('{}', response.content.decode())

        with self.assertRaises(LemmatizedTextBookmark.DoesNotExist):
            LemmatizedTextBookmark.objects.get(pk=bookmark.pk)
