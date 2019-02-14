from django.db import models


# this is for representing the lemmatized text

class LemmatizedText(models.Model):

    # this should be a JSON list of the form
    # [
    #   {"token": "res publica", "node": 1537, "resolved": true},
    #   {"token": "est", "node": 42, "resolved": false},
    #   ...
    # ]
    # where node is the pk of the LatticeNode

    data = models.TextField()
