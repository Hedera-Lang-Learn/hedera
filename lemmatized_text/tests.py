from django.test import TestCase, override_settings
from django.urls import reverse

from django.contrib.auth.models import User

from .models import LemmatizedText


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

    def test_token_node_dict(self):
        data = [
            {"word": "mis", "node": 3},
            {"word": "sim", "node": 55},
            {"word": "i", "node": 60},
            {"word": "i", "node": 60},
            {"word": "i", "node": 60},
            {"word": "ism", "node": None},
            {"word": "mis", "node": 22}
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
        self.assertEqual(lt.token_node_dict(), expected)

    def test_transform_data_to_html(self):
        data = [
            {"word": "mis", "node": 3, "resolved": True, "following": " "},
            {"word": "sim", "node": 55, "resolved": True, "following": " "},
            {"word": "i", "node": 60, "resolved": True, "following": ".\n"},
            {"word": "i", "node": 60, "resolved": True, "following": " "},
            {"word": "i", "node": 60, "resolved": True, "following": " "},
            {"word": "ism", "node": None, "resolved": False, "following": " "},
            {"word": "mis", "node": 22, "resolved": True, "following": "."}
        ]
        lt = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text="Femina somnia habet.",
            created_by=self.created_user1,
            data=data
        )

        expected = "<span node='3' resolved='True'>mis</span><span follower='true'> </span><span node='55' resolved='True'>sim</span><span follower='true'> </span><span node='60' resolved='True'>i</span><span follower='true'>.<br/></span><span node='60' resolved='True'>i</span><span follower='true'> </span><span node='60' resolved='True'>i</span><span follower='true'> </span><span node='None' resolved='False'>ism</span><span follower='true'> </span><span node='22' resolved='True'>mis</span><span follower='true'>.</span>"
        self.assertEqual(lt.transform_data_to_html(), expected)

    def test_handle_edited_data(self):
        data = [
            {"word": "Femina", "node": 3, "resolved": True, "following": " ", "word_normalized": "Femina"},
            {"word": "somnia", "node": 55, "resolved": False, "following": " ", "word_normalized": "somina"},
            {"word": "habet", "node": 60, "resolved": True, "following": ".", "word_normalized": "habet"},
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

        edited_text = "<span follower='true'> </span><span node='55' resolved='False' word_normalized='somina'>somnia something else</span><span follower='true'> </span><span node='60' resolved='True' word_normalized='habet'>habet</span><span follower='true'>. </span><span>And more!</span>"
        example_text.handle_edited_data("New title", edited_text)
        expected_edited_text = "<span node='None' resolved='True' word_normalized=''></span><span follower='true'> </span><span word_normalized='somnia' node='1' resolved='no-ambiguity'>somnia</span><span follower='true'> </span><span word_normalized='something' node='None' resolved='no-lemma'>something</span><span follower='true'> </span><span word_normalized='else' node='None' resolved='no-lemma'>else</span><span follower='true'>  </span><span node='60' resolved='True' word_normalized='habet'>habet</span><span follower='true'>. </span><span word_normalized='And' node='None' resolved='no-lemma'>And</span><span follower='true'> </span><span word_normalized='more' node='2' resolved='no-ambiguity'>more</span><span follower='true'>!</span>"
        self.assertEqual(example_text.transform_data_to_html(), expected_edited_text)
        self.assertEqual(example_text.token_count(), 7)
        self.assertEqual(example_text.original_text, " somnia something else habet. And more!")


class LemmatizedTextViewsTests(TestCase):

    def setUp(self):
        self.created_user1 = create_user("user1", "user1@example.com", "password")
        self.created_user2 = create_user("user2", "user2@example.com", "password2")

        data = [
            {"word": "mis", "node": 3, "resolved": True, "following": " "},
            {"word": "sim", "node": 55, "resolved": True, "following": " "},
            {"word": "i", "node": 60, "resolved": True, "following": ".\n"},
            {"word": "i", "node": 60, "resolved": True, "following": " "},
            {"word": "i", "node": 60, "resolved": True, "following": " "},
            {"word": "ism", "node": None, "resolved": False, "following": " "},
            {"word": "mis", "node": 22, "resolved": True, "following": "."}
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
        expected_initial_text = "<span node='3' resolved='True'>mis</span><span follower='true'> </span><span node='55' resolved='True'>sim</span><span follower='true'> </span><span node='60' resolved='True'>i</span><span follower='true'>.<br/></span><span node='60' resolved='True'>i</span><span follower='true'> </span><span node='60' resolved='True'>i</span><span follower='true'> </span><span node='None' resolved='False'>ism</span><span follower='true'> </span><span node='22' resolved='True'>mis</span><span follower='true'>.</span>"
        self.assertEqual(response.context["form"].initial["text"], expected_initial_text)

    def test_redirects_to_texts_list_on_success(self):
        self.client.login(username="user1", password="password")
        post_text = "<span node=3 resolved=True></span><span follower='true'> </span><span node=55 resolved=True>sim</span><span follower='true'> </span><span node=60 resolved=True>i</span><span follower='true'>.<br/></span><span node=60 resolved=True>i</span><span follower='true'> </span><span node=60 resolved=True>i</span><span follower='true'> </span><span node=None resolved=False>ism</span><span follower='true'> </span><span node=22 resolved=True>mis</span><span follower='true'>.</span>"
        response = self.client.post(reverse("lemmatized_text_edit", kwargs={"pk": self.lt.pk}), {"title": "Test title", "text": post_text})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/lemmatized_text/"))
