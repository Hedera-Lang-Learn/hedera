import logging

from django.db import models
from django.template.defaultfilters import floatformat
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from django_rq import get_connection, job
from iso639 import languages
from rq.job import Job, NoSuchJobError

from lemmatization.lemmatizer import Lemmatizer


def to_percent(val):
    return floatformat(val * 100, 2) + "%"


@job("default", timeout=600)
def lemmatize_text_job(text, lang, pk):
    try:
        obj = LemmatizedText.objects.get(pk=pk)

        def update(percentage):
            obj.completed = int(percentage * 100)
            obj.save()

        lemmatizer = Lemmatizer(lang, cb=update)
        obj.data = lemmatizer.lemmatize(text)
        obj.save()
    except Exception as e:
        logging.exception(e)
        raise e


# this is for representing the lemmatized text

class LemmatizedText(models.Model):

    title = models.CharField(max_length=100)
    lang = models.CharField(max_length=3)  # ISO 639.2
    cloned_from = models.ForeignKey("LemmatizedText", null=True, blank=True, on_delete=models.SET_NULL)
    cloned_for = models.ForeignKey("groups.Group", null=True, on_delete=models.SET_NULL)
    original_text = models.TextField()
    completed = models.IntegerField(default=0)

    # created_by is nullable because you can have Anonymous System Texts
    # 1. Anonymous System Texts
    # 2. Credited System Texts
    # 3. Private Texts - default
    public = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now)

    current_job = models.CharField(max_length=250, blank=True)

    # this should be a JSON list of the form
    # [
    #   {"word": "res publica", "following": " ", "node": 1537, "resolved": true},
    #   {"word": "est", "following": " ", "node": 42, "resolved": false},
    #   ...
    # ]
    # where node is the pk of the LatticeNode

    data = JSONField()

    def display_name(self):
        return languages.get(part3=self.lang).name

    def lemmatize(self):
        current_job = lemmatize_text_job.delay(self.original_text, self.lang, self.pk)
        self.current_job = current_job.id
        self.save()

    def lemmatization_job(self):
        try:
            return Job.fetch(self.current_job, get_connection())
        except NoSuchJobError:
            pass

    def cancel_lemmatization(self):
        lemmatization_job = self.lemmatization_job()
        if lemmatization_job and lemmatization_job.get_status() == "queued":
            lemmatization_job.cancel()
            self.current_job = ""
            self.save()

    def retry_lemmatization(self):
        lemmatization_job = self.lemmatization_job()
        if lemmatization_job and lemmatization_job.get_status() == "failed":
            lemmatization_job.requeue()
        else:
            self.cancel_lemmatization()
            self.lemmatize()

    def lemmatization_status(self):
        lemmatization_job = self.lemmatization_job()
        if lemmatization_job:
            return lemmatization_job.get_status()

    def can_cancel(self):
        return self.lemmatization_status() == "queued"

    def can_retry(self):
        if self.completed < 100:
            status = self.lemmatization_status()
            if status is None or status in ["finished", "failed"]:
                return True
        return False

    def __str__(self):
        return self.title

    def token_count(self):
        return len(self.data)

    def text(self):
        return "".join([d["word"] + d["following"] for d in self.data])

    def stats_for_user(self, user):
        stats = self.personalvocabularystats_set.filter(vocab_list__user=user).first()
        if stats:
            return {
                "unranked": to_percent(stats.unranked),
                "one": to_percent(stats.one),
                "two": to_percent(stats.two),
                "three": to_percent(stats.three),
                "four": to_percent(stats.four),
                "five": to_percent(stats.five),
            }

    @property
    def delete_url(self):
        return reverse("lemmatized_texts_delete", args=[self.pk])

    @property
    def clone_url(self):
        url = reverse("lemmatized_texts_create")
        return f"{url}?cloned_from={self.pk}"

    def api_data(self):
        return {
            "id": self.pk,
            "title": self.title,
            "lang": self.lang,
            "language": languages.get(part3=self.lang).name,
            "completed": self.completed,
            "tokenCount": self.token_count(),
            "lemmatizationStatus": self.lemmatization_status(),
            "createdAt": self.created_at,
            "canRetry": self.can_retry(),
            "canCancel": self.can_cancel(),
            "deleteUrl": self.delete_url,
            "cloneUrl": self.clone_url,
        }
