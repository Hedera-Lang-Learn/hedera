from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


LANG_CHOICES = [
    (lang, settings.HEDERA_LANGUAGES[lang])
    for lang in settings.HEDERA_LANGUAGES.keys()
]

ROLE_STUDENT = "student"
ROLE_LEARNER = "learner"
ROLE_TEACHER = "teacher"
ROLE_LANG_ADMIN = "langadmin"
ROLE_SUPER_ADMIN = "superadmin"

ROLE_CHOICES = [
    (ROLE_STUDENT, "Student in a Class"),
    (ROLE_LEARNER, "Lifelong Learner"),
    (ROLE_TEACHER, "Teacher"),
    (ROLE_LANG_ADMIN, "Language Admin"),
    (ROLE_SUPER_ADMIN, "Super user"),
]


class UserRole(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    lang = models.CharField(max_length=3, choices=LANG_CHOICES)

    class Meta:
        unique_together = [("user", "role", "lang")]
