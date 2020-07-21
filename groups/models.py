import uuid

from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from lemmatized_text.models import LemmatizedText
from vocab_list.models import VocabularyList


# class Course(models.Model):
#     pass

class Group(models.Model):
    """
    Respresents a Class but due to the reserved keyword of Class in Python we
    are using the more generic name "Group".
    """
    class_key = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    title = models.CharField(max_length=100)
    description = models.TextField()

    teachers = models.ManyToManyField(User, related_name="taught_classes")
    students = models.ManyToManyField(User, related_name="enrolled_classes")
    texts = models.ManyToManyField(LemmatizedText, related_name="classes")
    vocab_lists = models.ManyToManyField(VocabularyList, related_name="classes")

    student_invite_key = models.UUIDField(default=uuid.uuid4)
    teacher_invite_key = models.UUIDField(default=uuid.uuid4)

    def get_absolute_url(self):
        return reverse("groups_detail", args=[self.class_key])

    def roll_student_invite(self):
        self.student_invite_key = uuid.uuid4()
        self.save()

    def roll_teacher_invite(self):
        self.teacher_invite_key = uuid.uuid4()
        self.save()

    def students_join_link(self):
        domain = Site.objects.get_current().domain
        url = reverse("groups_join", args=[self.student_invite_key])
        return f"https://{domain}{url}"

    def teachers_join_link(self):
        domain = Site.objects.get_current().domain
        url = reverse("groups_join", args=[self.teacher_invite_key])
        return f"https://{domain}{url}"
