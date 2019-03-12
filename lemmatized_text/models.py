from django.contrib.postgres.fields import JSONField
from django.db import models


# this is for representing the lemmatized text

class LemmatizedText(models.Model):

    title = models.CharField(max_length=100)
    lang = models.CharField(max_length=3)  # ISO 639.2
    cloned_from = models.ForeignKey("LemmatizedText", null=True, blank=True, on_delete=models.SET_NULL)

    # this should be a JSON list of the form
    # [
    #   {"token": "res publica", "node": 1537, "resolved": true},
    #   {"token": "est", "node": 42, "resolved": false},
    #   ...
    # ]
    # where node is the pk of the LatticeNode

    data = JSONField()

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
