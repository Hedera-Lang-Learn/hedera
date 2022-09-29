import json
from uuid import uuid4

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from hedera.supported_languages import SUPPORTED_LANGUAGES
from hedera.tests import utils
from lemmatized_text.models import LemmatizedTextBookmark
from vocab_list.models import (
    PersonalVocabularyList,
    PersonalVocabularyListEntry
)


class PersonalVocabularyQuickAddAPITest(APITestCase):

    def setUp(self):
        test_username = f"test_user_{uuid4()}"
        self.created_user = User.objects.create_user(username=test_username, email=f"{test_username}@test.com", password="password")
        self.client.force_login(user=self.created_user)
        self.personal_vocab_list = PersonalVocabularyList.objects.create(user=self.created_user, lang="lat")
        data = {
            "familiarity": 1,
            "headword": "testers",
            "definition": "therefore",
            "vocabulary_list_id": self.personal_vocab_list.id
        }
        self.personal_vocab_list_entry = PersonalVocabularyListEntry.objects.create(**data)

    def test_fail_get_personal_vocabulary_quick_add_api(self):
        test_username = f"test_user_{uuid4()}"
        self.created_user = User.objects.create_user(username=test_username, email=f"{test_username}@test.com", password="password")
        self.client.force_login(user=self.created_user)
        response = self.client.get("/api/v1/personal_vocab_list/quick_add/")
        self.assertEqual(len(response.json()["data"]), 0)

    def test_get_personal_vocabulary_quick_add_api(self):
        response = self.client.get("/api/v1/personal_vocab_list/quick_add/")
        self.assertEqual(response.status_code, 200)

    def test_post_personal_vocabulary_quick_add_api_with_id(self):
        payload = {
            "familiarity": 1,
            "definition": "something",
            "headword": "sum",
            "vocabulary_list_id": self.personal_vocab_list.id,
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_post_personal_vocabulary_quick_add_api_no_id(self):
        payload = {
            "familiarity": 1,
            "definition": "something",
            "headword": "sum",
            "vocabulary_list_id": None,
            "lang": "lat"
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_fail_post_personal_vocabulary_quick_add_api_no_id_no_lang(self):
        payload = {
            "familiarity": 1,
            "definition": "something",
            "headword": "sum",
            "vocabulary_list_id": None
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "'lang field not provided'")

    def test_fail_post_personal_vocabulary_quick_add_api_missing_vocab_list_id(self):
        payload = {
            "familiarity": 1,
            "definition": "something",
            "headword": "sum",
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_fail_post_personal_vocabulary_quick_add_api_missing_familiarity(self):
        payload = {
            "definition": "something",
            "headword": "sum",
            "vocabulary_list_id": self.personal_vocab_list.id,
        }
        response = self.client.post("/api/v1/personal_vocab_list/quick_add/", json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_fail_post_personal_vocabulary_quick_add_api_missing_definition(self):
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
            "definition": "something",
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


class MeAPITest(APITestCase):
    def setUp(self):
        test_username = f"test_user_{uuid4()}"
        self.created_user = User.objects.create_user(username=test_username, email=f"{test_username}@test.com", password="password")
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


class SupportedLanguagesAPITest(APITestCase):

    def setUp(self):
        self.user = utils.create_user()
        self.client.force_login(user=self.user)

    def test_get_supported_language_list(self):
        languages = [[lang.code, lang.verbose_name] for lang in SUPPORTED_LANGUAGES.values()]
        response = self.client.get(f"/api/v1/supported_languages/", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], languages)


class TokenHistoryAPITest(APITestCase):
    def setUp(self):
        self.is_teacher = utils.create_user()
        self.is_student = utils.create_user()
        self.is_invalid_user = utils.create_user()
        self.text = utils.create_lemmatized_text(data=[{"node": None, "word": "Lorem", "resolved": "no-lemma", "following": " ", "word_normalized": "Lorem"}], created_by=self.is_teacher)
        self.create_class = utils.create_group(teacher=self.is_teacher, student=self.is_student, text=self.text)
        self.public_text = utils.create_lemmatized_text(data=[{"node": None, "word": "Lorem", "resolved": "no-lemma", "following": " ", "word_normalized": "Lorem"}], created_by=self.is_teacher, public=True)

    def test_successful_get_public_lemmatized_tokens(self):
        self.client.force_login(user=self.is_invalid_user)
        response = self.client.get(f"/api/v1/lemmatized_texts/{self.public_text.pk}/tokens/0/history/")
        self.client.logout()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

    def test_successful_get_lemmatized_tokens_is_student(self):
        self.client.force_login(user=self.is_student)
        response = self.client.get(f"/api/v1/lemmatized_texts/{self.text.pk}/tokens/0/history/")
        self.client.logout()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

    def test_successful_get_lemmatized_tokens_is_teacher(self):
        self.client.force_login(user=self.is_teacher)
        response = self.client.get(f"/api/v1/lemmatized_texts/{self.text.pk}/tokens/0/history/")
        self.client.logout()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

    def test_unsuccessful_get_lemmatized_tokens(self):
        self.client.force_login(user=self.is_invalid_user)
        response = self.client.get(f"/api/v1/lemmatized_texts/{self.text.pk}/tokens/0/history/")
        self.client.logout()
        self.assertEqual(response.status_code, 404)

    def test_unsuccessful_get_lemmatized_tokens_no_account(self):
        response = self.client.get(f"/api/v1/lemmatized_texts/{self.text.pk}/tokens/0/history/")
        self.assertEqual(response.status_code, 401)
