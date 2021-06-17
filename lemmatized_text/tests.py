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
        lemmatized_text = LemmatizedText.objects.create(
            title="Test title",
            lang="lat",
            original_text="Femina somnia habet.",
            created_by=self.created_user1,
            data=json.dumps({"key": "test"})
        )
        self.assertEqual(LemmatizedText.objects.all().count(), 1)
        lemmatized_text.clone()
        self.assertEqual(LemmatizedText.objects.all().count(), 2)
        lemmatized_text.clone(cloned_by=self.created_user2)
        self.assertEqual(LemmatizedText.objects.all().count(), 3)
        self.assertEqual(LemmatizedText.objects.filter(created_by=self.created_user1).count(), 2)
        self.assertEqual(LemmatizedText.objects.filter(created_by=self.created_user2).count(), 1)
