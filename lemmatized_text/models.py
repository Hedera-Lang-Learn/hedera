from django.db import models

from django.contrib.postgres.fields import JSONField

from django_rq import job

from lemmatization.lemmatizer import Lemmatizer


@job
def lemmatize_text_job(text, lang, pk):
    obj = LemmatizedText.objects.get(pk=pk)

    def update(percentage):
        obj.completed = int(percentage * 100)
        obj.save()

    lemmatizer = Lemmatizer(lang, cb=update)
    obj.data = lemmatizer.lemmatize(text)
    obj.save()


# this is for representing the lemmatized text

class LemmatizedText(models.Model):

    title = models.CharField(max_length=100)
    lang = models.CharField(max_length=3)  # ISO 639.2
    cloned_from = models.ForeignKey("LemmatizedText", null=True, blank=True, on_delete=models.SET_NULL)

    completed = models.IntegerField(default=0)

    # this should be a JSON list of the form
    # [
    #   {"token": "res publica", "node": 1537, "resolved": true},
    #   {"token": "est", "node": 42, "resolved": false},
    #   ...
    # ]
    # where node is the pk of the LatticeNode

    data = JSONField()

    def lemmatize(self, text, lang):
        lemmatize_text_job.delay(text, lang, self.pk)

    def __str__(self):
        return self.title

    def token_count(self):
        return len(self.data)

    def text(self):
        return " ".join([d["token"] for d in self.data])

    def api_data(self):
        return {
            "id": self.pk,
            "title": self.title,
            "lang": self.lang,
        }
