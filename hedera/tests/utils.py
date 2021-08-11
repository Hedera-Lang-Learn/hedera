from django.contrib.auth import get_user_model

from lemmatized_text.models import LemmatizedText, LemmatizedTextBookmark


User = get_user_model()


def create_user(**kwargs):
    count = User.objects.all().count()
    if "username" not in kwargs:
        kwargs["username"] = f"test_user{count}"
    if "email" not in kwargs:
        kwargs["email"] = "%s@test.hederaproject.org" % kwargs["username"]
    if "password" not in kwargs:
        kwargs["password"] = "not_a_real_password"

    return User.objects.create_user(**kwargs)


def create_lemmatized_text(**kwargs):
    count = LemmatizedText.objects.all().count()
    if "title" not in kwargs:
        kwargs["title"] = f"lemmatized_text{count}"
    if "lang" not in kwargs:
        kwargs["lang"] = "lat"
    if "original_text" not in kwargs:
        kwargs["original_text"] = f"[{count}] Gallia est omnis divisa in partes tres "
    if "public" not in kwargs:
        kwargs["public"] = False
    if "completed" not in kwargs:
        kwargs["completed"] = 100
    if "data" not in kwargs:
        kwargs["data"] = []
    if "created_by" not in kwargs:
        kwargs["created_by"] = create_user()

    return LemmatizedText.objects.create(**kwargs)


def create_bookmark(**kwargs):
    if "user" not in kwargs:
        kwargs["user"] = create_user()
    if "text" not in kwargs:
        kwargs["text"] = create_lemmatized_text()

    return LemmatizedTextBookmark.objects.create(**kwargs)
