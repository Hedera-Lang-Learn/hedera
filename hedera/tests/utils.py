from django.contrib.auth import get_user_model

from groups.models import Group
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


def create_group(**kwargs):
    count = Group.objects.all().count()
    if "title" not in kwargs:
        kwargs["title"] = f"classes_{count}"
    if "description" not in kwargs:
        kwargs["description"] = "testing"
    teacher = kwargs["teacher"] if "teacher" in kwargs else create_user(username="teacher")
    group_instance = Group.objects.create(title=kwargs["title"], description=kwargs["description"], created_by=teacher)
    #Note: We use set() method because django does not allow passing many-to-many relationships directly in kwargs when creating the group
    student = kwargs["student"] if "student" in kwargs else create_user(username="student")
    text = kwargs["text"] if "text" in kwargs else create_lemmatized_text()
    group_instance.teachers.set([teacher])
    group_instance.students.set([student])
    group_instance.texts.set([text])
    return group_instance
