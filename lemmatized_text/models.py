import json
import logging
import uuid
from collections import defaultdict
from html import escape

from django.conf import settings
from django.db import models
from django.template.defaultfilters import floatformat
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth.models import User

from django_rq import get_connection, job
from iso639 import languages
from rq.job import Job, NoSuchJobError

from lemmatization.lemmatizer import Lemmatizer
from lemmatization.models import Lemma

from .parsers import EditedTextHtmlParser, TagStripper


logger = logging.getLogger(__name__)


def to_percent(val):
    return floatformat(val * 100, 2) + "%"


def parse_following(follower):
    """
    Used to parse new lines and carriage returns in the following tokens
    Ex: "\r\n\n\n" => "<br/><br/><br/>"
    Note: We are mutating the follower tokens
    """
    if "\r\n" in follower:
        follower = follower.replace("\r\n", "<br/>")
    if "\n" in follower:
        follower = follower.replace("\n", "<br/>")
    return follower


def transform_token_to_html(token):
    token_data = {k: v for k, v in token.items() if k not in ("word", "following")}
    return (
        f'<span data-token="{escape(json.dumps(token_data))}">'
        f"{token['word']}</span><span follower='true'>"
        f"{parse_following(token['following'])}</span>")


def transform_data_to_html(data):
    return "".join([transform_token_to_html(token) for token in data])


@job("default", timeout=600)
def lemmatize_text_job(text, lang, pk):
    try:
        logger.info(f"start lemmatize_text_job {lang} {pk}")
        obj = LemmatizedText.objects.get(pk=pk)

        def update(percentage):
            logger.debug(f"update lemmatize_text_job {lang} {pk} {percentage:.1%}")
            obj.completed = int(percentage * 100)
            obj.save()

        lemmatizer = Lemmatizer(lang, cb=update)
        obj.data = lemmatizer.lemmatize(text)
        obj.save()
        logger.info(f"end lemmatize_text_job {lang} {pk}")
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

    data = models.JSONField()

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

    def update_token(self, user, token_index, lemma_id, gloss_ids, resolved):
        self.data[token_index]["lemma_id"] = lemma_id
        self.data[token_index]["gloss_ids"] = gloss_ids
        self.data[token_index]["resolved"] = resolved
        self.save()
        self.logs.create(
            user=user,
            token_index=token_index,
            lemma_id=lemma_id,
            resolved=resolved,
        )

    def handle_edited_data(self, title, edits):
        self.title = title
        # Note: Modified with the carriage return and new line to match newline edits we test in LemmatizedTextTests. This should not impact the application
        cleaned_edits = edits.replace("<p>", "").replace("</p>", "<br/>").replace("<br/>", "\r\n")
        edit_parser = EditedTextHtmlParser(
            token_lemma_dict=self.token_lemma_dict(),
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

    def token_lemma_dict(self):
        lemma_dict = defaultdict(list)
        for token in self.data:
            lemma_dict[token["word"]].append(token["lemma_id"])
        return dict(lemma_dict)

    def transform_data_to_html(self):
        return transform_data_to_html(self.data)

    def transform_data_to_glossary(self):
        """Returns a list of words used in the text with their full glosses."""
        lemma_ids = [token["lemma_id"] for token in self.data if token.get("lemma_id")]
        lemma_queryset = Lemma.objects.filter(pk__in=lemma_ids).order_by("label")
        glossary = []
        for lemma_object in lemma_queryset:
            glossary.append({
                "label": lemma_object.label,
                "glosses": [gloss_object.gloss for gloss_object in lemma_object.glosses.all()],
            })
        return glossary

    def is_valid_user(self, user):
        """
        check if user has the filtered_group ids in their enrolled classes or taught classes
        Note: only checks if user is related to at least one class with the same text/group id
        """
        groups = self.classes.all()
        filtered_groups = groups.filter(texts__in=[self.pk])
        enrolled_classes = user.enrolled_classes.all()
        taught_classes = user.taught_classes.all()
        is_student = False
        is_teacher = False
        is_public = self.public
        is_created_by = self.created_by
        for fg in filtered_groups:
            is_student = enrolled_classes.filter(pk=fg.pk).exists()
            is_teacher = taught_classes.filter(pk=fg.pk).exists()
        return any([is_student, is_teacher, is_public, is_created_by.pk == user.pk]) is True


class LemmatizationLog(models.Model):
    # Who
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # Changed What Attributes
    token_index = models.IntegerField()

    lemma = models.ForeignKey(Lemma, null=True, on_delete=models.CASCADE)

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
            lemma_id=self.lemma_id,
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
