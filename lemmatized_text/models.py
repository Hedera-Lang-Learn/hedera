import logging
import uuid
from collections import defaultdict

from django.conf import settings
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

from .parsers import EditedTextHtmlParser, TagStripper


def to_percent(val):
    return floatformat(val * 100, 2) + "%"


def parse_following(follower):
    return follower.replace("\n", "<br/>")


def format_token_key_value_pairs(token):
    return " ".join([f"{k}='{v}'" for k, v in token.items() if k not in ("word", "following")])


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
    cloned_for = models.ForeignKey("groups.Group", null=True, blank=True, on_delete=models.SET_NULL)
    original_text = models.TextField()
    completed = models.IntegerField(default=0)

    secret_id = models.UUIDField(default=uuid.uuid4, editable=False)

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
    def learner_url(self):
        return reverse("lemmatized_texts_learner", args=[self.pk])

    @property
    def handout_url(self):
        return reverse("lemmatized_texts_handout", args=[self.secret_id])

    @property
    def delete_url(self):
        return reverse("lemmatized_texts_delete", args=[self.pk])

    @property
    def clone_url(self):
        url = reverse("lemmatized_texts_create")
        return f"{url}?cloned_from={self.pk}"

    @property
    def edit_url(self):
        return reverse("lemmatized_text_edit", args=[self.pk])

    def clone(self, cloned_by=None):
        """Set a copy of this object's pk to None, set some relationships and save (cloning)"""
        # https://docs.djangoproject.com/en/3.2/topics/db/queries/#copying-model-instances
        obj = LemmatizedText.objects.get(pk=self.pk)  # declaring 'self' here results in a ValueError
        obj.pk = None
        obj.cloned_from = self
        obj.created_by = cloned_by or self.created_by
        obj.secret_id = uuid.uuid4()
        obj.created_at = timezone.now()
        obj.title += " (clone)"
        obj.save()
        return obj

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
            "editUrl": self.edit_url,
            "clonedFrom": self.cloned_from.pk if self.cloned_from else None,
            "clonedFor": self.cloned_for.pk if self.cloned_for else None,
            "requireClone": self.classes.all().count() > 0,
            "handoutUrl": self.handout_url,
            "learnerUrl": self.learner_url,
        }

    def update_token(self, user, token_index, node_id, resolved):
        self.data[token_index]["node"] = node_id
        self.data[token_index]["resolved"] = resolved
        self.save()
        self.logs.create(
            user=user,
            token_index=token_index,
            node_id=node_id,
            resolved=resolved,
        )

    def handle_edited_data(self, title, edits):
        self.title = title

        cleaned_edits = edits.replace("<p>", "").replace("</p>", "<br/>").replace("<br/>", "\n")
        edit_parser = EditedTextHtmlParser(
            token_node_dict=self.token_node_dict(),
            lang=self.lang
        )
        edit_parser.feed(cleaned_edits)

        # Trimming junk tokens that get appended to the end of the list
        for token in reversed(edit_parser.lemmatized_text_data):
            if token["word"] != "":
                break
            edit_parser.lemmatized_text_data.remove(token)
        self.data = edit_parser.lemmatized_text_data

        strip_parser = TagStripper()
        strip_parser.feed(cleaned_edits)
        self.original_text = strip_parser.get_data()
        self.save()

    def token_node_dict(self):
        lemma_dict = defaultdict(list)
        for token in self.data:
            lemma_dict[token["word"]].append(token["node"])
        return dict(lemma_dict)

    def transform_data_to_html(self):
        return "".join([
            (
                f"<span {format_token_key_value_pairs(token)}>"
                f"{token['word']}</span><span follower='true'>"
                f"{parse_following(token['following'])}</span>"
            )
            for token in self.data
        ])


class LemmatizationLog(models.Model):
    # Who
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # Changed What Attributes
    token_index = models.IntegerField()
    node = models.ForeignKey("lattices.LatticeNode", on_delete=models.CASCADE)
    resolved = models.CharField(max_length=100)

    # On What Text
    text = models.ForeignKey(LemmatizedText, on_delete=models.CASCADE, related_name="logs")

    # When
    created_at = models.DateTimeField(default=timezone.now)

    def data(self):
        return dict(
            id=self.pk,
            user=self.user.email,
            tokenIndex=self.token_index,
            node=self.node.pk,
            resolves=self.resolved,
            text=self.text.pk,
            createdAt=self.created_at
        )


class LemmatizedTextBookmark(models.Model):
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        on_delete=models.CASCADE
    )
    text = models.ForeignKey(LemmatizedText, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "lemmatized text bookmark"
        verbose_name_plural = "lemmatized text bookmarks"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "text"], name="unique_lemmatized_text_bookmark")
        ]

    def api_data(self):
        return dict(
            id=self.pk,
            userId=self.user.pk,
            createdAt=self.created_at,
            text=self.text.api_data(),
        )

    def __str__(self):
        return f"{self.user} lemmatized text bookmark: {self.text}"
