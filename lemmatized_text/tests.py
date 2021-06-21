import json

from django.test import TestCase, override_settings

from django.contrib.auth.models import User

from .models import LemmatizedText


@override_settings(
    AUTHENTICATION_BACKENDS=[
        "account.auth_backends.EmailAuthenticationBackend"
    ]
)
class LemmatizedTextTests(TestCase):

    def create_user(self, username, email, password):
        user = User.objects.create_user(username, email=email, password=password)
        return user

    def setUp(self):
        self.created_user1 = self.create_user("user1", "user1@example.com", "password")
        self.created_user2 = self.create_user("user2", "user2@example.com", "password2")

    def test_clone(self):
        lt = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text="Femina somnia habet.",
            created_by=self.created_user1,
            data=json.dumps({"key": "test"})
        )
        lt_clone = lt.clone()
        self.assertEqual(LemmatizedText.objects.all().count(), 2)
        lt.clone(cloned_by=self.created_user2)
        self.assertEqual(LemmatizedText.objects.all().count(), 3)
        self.assertEqual(LemmatizedText.objects.filter(created_by=self.created_user1).count(), 2)
        self.assertEqual(LemmatizedText.objects.filter(created_by=self.created_user2).count(), 1)
        self.assertEqual(lt.title, lt_clone.title)
        self.assertEqual(lt.lang, lt_clone.lang)
        self.assertEqual(lt.original_text, lt_clone.original_text)
        self.assertEqual(lt.data, lt_clone.data)
        self.assertNotEqual(lt.secret_id, lt_clone.secret_id)
        self.assertNotEqual(lt.created_at, lt_clone.created_at)

