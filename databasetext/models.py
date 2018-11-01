from django.db import models


# note that this is not for managing all the metadata around a text but is
# merely a lightweight storage for texts akin to a keystore.

class Text(models.Model):
    text = models.TextField()
