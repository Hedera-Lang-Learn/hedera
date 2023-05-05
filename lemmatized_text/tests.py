from django.test import TestCase, override_settings
from django.urls import reverse

from django.contrib.auth.models import User

from .models import Lemma, LemmatizedText, transform_data_to_html
from .test_data import (
    expected_lemmatized_text_edit_underscore,
    test_lemma_list,
    test_lemmatized_no_extra_tokens,
    test_lemmatized_no_underscore_text,
    test_lemmatized_text,
    test_original_text,
    test_text_edit_underscore
)


def create_user(username, email, password):
    user = User.objects.create_user(username, email=email, password=password)
    return user


@override_settings(
    AUTHENTICATION_BACKENDS=[
        "account.auth_backends.EmailAuthenticationBackend"
    ]
)
class LemmatizedTextTests(TestCase):

    def setUp(self):
        self.created_user1 = create_user("user1", "user1@example.com", "password")
        self.created_user2 = create_user("user2", "user2@example.com", "password2")
        self.data_html = transform_data_to_html(test_lemmatized_text)

    def test_clone(self):
        lt = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text="Femina somnia habet.",
            created_by=self.created_user1,
            data={"key": "test"}
        )
        lt_clone = lt.clone()
        self.assertEqual(LemmatizedText.objects.all().count(), 2)
        lt.clone(cloned_by=self.created_user2)
        self.assertEqual(LemmatizedText.objects.all().count(), 3)
        self.assertEqual(LemmatizedText.objects.filter(created_by=self.created_user1).count(), 2)
        self.assertEqual(LemmatizedText.objects.filter(created_by=self.created_user2).count(), 1)
        self.assertEqual(lt_clone.title, f"{lt.title} (clone)")
        self.assertEqual(lt.lang, lt_clone.lang)
        self.assertEqual(lt.original_text, lt_clone.original_text)
        self.assertEqual(lt.data, lt_clone.data)
        self.assertNotEqual(lt.secret_id, lt_clone.secret_id)
        self.assertNotEqual(lt.created_at, lt_clone.created_at)

    def test_token_lemma_dict(self):
        data = [
            {"word": "mis", "lemma_id": 3},
            {"word": "sim", "lemma_id": 55},
            {"word": "i", "lemma_id": 60},
            {"word": "i", "lemma_id": 60},
            {"word": "i", "lemma_id": 60},
            {"word": "ism", "lemma_id": None},
            {"word": "mis", "lemma_id": 22}
        ]
        lt = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text="Femina somnia habet.",
            created_by=self.created_user1,
            data=data
        )
        expected = {
            "mis": [3, 22],
            "sim": [55],
            "i": [60, 60, 60],
            "ism": [None]
        }
        self.assertEqual(lt.token_lemma_dict(), expected)

    def test_transform_data_to_html(self):
        data = [
            {"word": "mis", "lemma_id": 3, "resolved": True, "gloss_ids": [], "glossed": "na", "following": " "},
            {"word": "sim", "lemma_id": 55, "resolved": True, "gloss_ids": [], "glossed": "na", "following": " "},
            {"word": "i", "lemma_id": 60, "resolved": True, "gloss_ids": [], "glossed": "na", "following": ".\n"},
            {"word": "i", "lemma_id": 60, "resolved": True, "gloss_ids": [], "glossed": "na", "following": " "},
            {"word": "i", "lemma_id": 60, "resolved": True, "gloss_ids": [], "glossed": "na", "following": " "},
            {"word": "ism", "lemma_id": None, "resolved": False, "gloss_ids": [], "glossed": "na", "following": " "},
            {"word": "mis", "lemma_id": 22, "resolved": True, "gloss_ids": [], "glossed": "na", "following": "."}
        ]
        lt = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text="Femina somnia habet.",
            created_by=self.created_user1,
            data=data
        )

        # TODO: Figure out how to do these HTML tests better / less brittle
        expected = """<span data-token="{&quot;lemma_id&quot;: 3, &quot;resolved&quot;: true, &quot;gloss_ids&quot;: [], &quot;glossed&quot;: &quot;na&quot;}">mis</span><span follower='true'> </span><span data-token="{&quot;lemma_id&quot;: 55, &quot;resolved&quot;: true, &quot;gloss_ids&quot;: [], &quot;glossed&quot;: &quot;na&quot;}">sim</span><span follower='true'> </span><span data-token="{&quot;lemma_id&quot;: 60, &quot;resolved&quot;: true, &quot;gloss_ids&quot;: [], &quot;glossed&quot;: &quot;na&quot;}">i</span><span follower='true'>.<br/></span><span data-token="{&quot;lemma_id&quot;: 60, &quot;resolved&quot;: true, &quot;gloss_ids&quot;: [], &quot;glossed&quot;: &quot;na&quot;}">i</span><span follower='true'> </span><span data-token="{&quot;lemma_id&quot;: 60, &quot;resolved&quot;: true, &quot;gloss_ids&quot;: [], &quot;glossed&quot;: &quot;na&quot;}">i</span><span follower='true'> </span><span data-token="{&quot;lemma_id&quot;: null, &quot;resolved&quot;: false, &quot;gloss_ids&quot;: [], &quot;glossed&quot;: &quot;na&quot;}">ism</span><span follower='true'> </span><span data-token="{&quot;lemma_id&quot;: 22, &quot;resolved&quot;: true, &quot;gloss_ids&quot;: [], &quot;glossed&quot;: &quot;na&quot;}">mis</span><span follower='true'>.</span>"""
        self.assertEqual(lt.transform_data_to_html(), expected)

    def test_transform_data_to_html_with_newlines(self):
        lt = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text=test_original_text,
            created_by=self.created_user1,
            data=test_lemmatized_text
        )
        self.assertEqual(lt.transform_data_to_html(), self.data_html)

    def test_handle_edited_data(self):
        data = [
            {"word": "Femina", "lemma_id": 3, "resolved": True, "following": " ", "gloss_ids": [], "glossed": "na", "word_normalized": "Femina"},
            {"word": "somnia", "lemma_id": 55, "resolved": False, "following": " ", "gloss_ids": [], "glossed": "na", "word_normalized": "somina"},
            {"word": "habet", "lemma_id": 60, "resolved": True, "following": ".", "gloss_ids": [], "glossed": "na", "word_normalized": "habet"},
        ]

        example_text = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text="Femina somnia habet.",
            created_by=self.created_user1,
            data=data
        )
        self.assertEqual(example_text.token_count(), 3)
        self.assertEqual(example_text.original_text, "Femina somnia habet.")

        # modify HTML, mimicking what's happening in the WYSIWYG
        html = transform_data_to_html(data)
        html = html.replace(data[0]["word"], data[0]["word"] + " virtus imperator")
        html = html.replace(data[2]["word"], "pecunia " + data[-1]["word"])

        # handle edits and sanity check the result
        example_text.handle_edited_data("New title", html)
        self.assertEqual(example_text.original_text, "Femina virtus imperator somnia pecunia habet.")
        self.assertEqual(example_text.token_count(), 6)

        # check the individual token words
        words_post_edit = [token["word"] for token in example_text.data]
        self.assertIn("virtus", words_post_edit)
        self.assertIn("imperator", words_post_edit)
        self.assertIn("somnia", words_post_edit)
        self.assertIn("pecunia", words_post_edit)

    def test_handle_edited_data_no_changes(self):
        example_text = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text=test_original_text,
            created_by=self.created_user1,
            data=test_lemmatized_text
        )
        self.assertEqual.__self__.maxDiff = None
        example_text.handle_edited_data("Test title", self.data_html)
        self.assertEqual(example_text.data, test_lemmatized_text)
        self.assertEqual(example_text.token_count(), len(test_lemmatized_text))

    def test_handle_edited_data_add_newline(self):
        example_text = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text=test_original_text,
            created_by=self.created_user1,
            data=test_lemmatized_text
        )
        test_lemmatized_text[0]["following"] = "\r\n"
        test_edited_text_html = transform_data_to_html(test_lemmatized_text)
        example_text.handle_edited_data("Test title", test_edited_text_html)
        self.assertEqual(example_text.token_count(), len(test_lemmatized_text))

    def test_handle_edited_data_underscore(self):
        """
        Example expected behavior
            text without underscore - token_lemma_dict={'contristatus': [13339], 'est': [1225]}
            edited text with underscore - token_lemma_dict={'': [13339, 1225], 'contristatus est': [13339]}
        """
        example_text = LemmatizedText.objects.create(
            title="Test underscore edit",
            lang="lat",
            original_text="contristatus est",
            created_by=self.created_user1,
            data=test_lemmatized_no_underscore_text
        )
        example_text.handle_edited_data("Test title", "contristatus_est")
        self.assertEqual("contristatus est" in example_text.token_lemma_dict(), True)

    def test_handle_edited_data_underscore_long_text(self):

        example_text = LemmatizedText.objects.create(
            title="Test add text with underscore",
            lang="lat",
            original_text=test_original_text,
            created_by=self.created_user1,
            data=test_lemmatized_text
        )
        test_text_html = transform_data_to_html(test_lemmatized_text)
        # insert edited text at the end of a closing </span> element
        index_to_insert_edit = test_text_html.find("</span>")
        test_edited_text_html = test_text_html[:index_to_insert_edit] + "\n\rcontristatus_est" + test_text_html[index_to_insert_edit:]
        example_text.handle_edited_data("Test title", test_edited_text_html)
        self.assertEqual("contristatus est" in example_text.token_lemma_dict(), True)

    def test_handle_edited_data_underscore_no_extra_tokens(self):
        for lemma in test_lemma_list:
            created_lemma = Lemma(**lemma)
            created_lemma.save()

        example_text = LemmatizedText.objects.create(
            title="Test edit with underscore",
            lang="lat",
            original_text=test_text_edit_underscore,
            created_by=self.created_user1,
            data=test_lemmatized_no_extra_tokens
        )

        test_text_no_underscore_html = transform_data_to_html(test_lemmatized_no_extra_tokens)
        test_edited_text_with_underscore_html = test_text_no_underscore_html.replace(">dēlenda<", ">dēlenda_<")
        example_text.handle_edited_data("Test title", test_edited_text_with_underscore_html)
        self.assertEqual(example_text.data, expected_lemmatized_text_edit_underscore)


class LemmatizedTextViewsTests(TestCase):

    def setUp(self):
        self.created_user1 = create_user("user1", "user1@example.com", "password")
        self.created_user2 = create_user("user2", "user2@example.com", "password2")
        self.data_html = transform_data_to_html(test_lemmatized_text)

        data = [
            {"word": "mis", "lemma_id": 3, "resolved": True, "following": " "},
            {"word": "sim", "lemma_id": 55, "resolved": True, "following": " "},
            {"word": "i", "lemma_id": 60, "resolved": True, "following": ".\n"},
            {"word": "i", "lemma_id": 60, "resolved": True, "following": " "},
            {"word": "i", "lemma_id": 60, "resolved": True, "following": " "},
            {"word": "ism", "lemma_id": None, "resolved": False, "following": " "},
            {"word": "mis", "lemma_id": 22, "resolved": True, "following": "."}
        ]
        self.lt = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text="mis sim i.\ni i ism mis.",
            created_by=self.created_user1,
            data=data
        )
        self.lt2 = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text="mis sim i.\ni i ism mis.",
            created_by=self.created_user2,
            data=data
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("lemmatized_text_edit", kwargs={"pk": self.lt.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/account/login/"))

    def test_404_if_logged_in_but_not_user_text(self):
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse("lemmatized_text_edit", kwargs={"pk": self.lt2.pk}))
        self.assertEqual(response.status_code, 404)

    def test_404_if_text_does_not_exist(self):
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse("lemmatized_text_edit", kwargs={"pk": 10000}))
        self.assertEqual(response.status_code, 404)

    def test_uses_edit_template(self):
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse("lemmatized_text_edit", kwargs={"pk": self.lt.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "lemmatized_text/edit.html")

    def test_form_inital_text_value(self):
        self.client.login(username="user1", password="password")
        response = self.client.get(reverse("lemmatized_text_edit", kwargs={"pk": self.lt.pk}))
        self.assertEqual(response.status_code, 200)
        expected_initial_text = """<span data-token="{&quot;lemma_id&quot;: 3, &quot;resolved&quot;: true}">mis</span><span follower='true'> </span><span data-token="{&quot;lemma_id&quot;: 55, &quot;resolved&quot;: true}">sim</span><span follower='true'> </span><span data-token="{&quot;lemma_id&quot;: 60, &quot;resolved&quot;: true}">i</span><span follower='true'>.<br/></span><span data-token="{&quot;lemma_id&quot;: 60, &quot;resolved&quot;: true}">i</span><span follower='true'> </span><span data-token="{&quot;lemma_id&quot;: 60, &quot;resolved&quot;: true}">i</span><span follower='true'> </span><span data-token="{&quot;lemma_id&quot;: null, &quot;resolved&quot;: false}">ism</span><span follower='true'> </span><span data-token="{&quot;lemma_id&quot;: 22, &quot;resolved&quot;: true}">mis</span><span follower='true'>.</span>"""
        self.assertEqual(response.context["form"].initial["text"], expected_initial_text)

    def test_redirects_to_texts_list_on_success(self):
        self.client.login(username="user1", password="password")
        response = self.client.post(reverse("lemmatized_text_edit", kwargs={"pk": self.lt.pk}), {"title": "Test title", "text": self.data_html})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/lemmatized_text/"))
