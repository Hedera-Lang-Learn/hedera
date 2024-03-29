from django.db import models


class LatticeNode(models.Model):

    label = models.TextField()
    gloss = models.TextField()
    canonical = models.BooleanField(default=False)
    children = models.ManyToManyField("self", symmetrical=False, related_name="parents")

    def __str__(self):
        return self.label + (" [canonical]" if self.canonical else "")

    def related_nodes(self, up=True, down=True):
        nodes = [self]
        if self.children.count() == 1 and down:
            child = self.children.first()
            nodes += child.related_nodes(up=False)
        if self.parents.count() > 0 and up:
            for parent in self.parents.all():
                nodes += parent.related_nodes(down=False)
        return nodes

    def gloss_data(self):
        return dict(
            pk=self.pk,
            gloss=self.gloss,
            label=self.label,
            canonical=self.canonical,
        )

    def to_dict(self, up=True, down=True):
        """
        serialises the node with its form/lemma strings and descendants
        """
        d = {
            "pk": self.pk,
            "label": self.label,
            "gloss": self.gloss,
            "canonical": self.canonical,
            "lemmas": [
                {
                    "lemma": lemma_node.lemma,
                    "context": lemma_node.context,
                } for lemma_node in self.lemma_strings.all()
            ],
            "vocabulary_entries": [  # @@@ temporarily here
                {
                    "headword": entry.headword,
                    "gloss": entry.gloss,
                } for entry in self.vocabulary_entries.all()
            ],
        }
        if down:
            d.update({
                "children": [
                    child.to_dict(up=False) for child in self.children.all()
                ],
            })
        if up:
            d.update({
                "parents": [
                    parent.to_dict(down=False) for parent in self.parents.all()
                ],
            })

        return d


class LemmaNode(models.Model):
    """
    mapping from lemma string to lattice node (in a given context)

    This effectively defines a node in a lattice as "meaning" anything
    with a lemma of this string. If the lemma string is ambiguous, or has
    multiple senses to be distinguished, the referenced node can have a child
    for each possibility.

    The "context" is just an optional label to clarify interpretation if a
    form coming from one place should be treated differently from one coming
    from another place. For example, "sum1" might mean one thing coming from
    Morpheus but another coming from a different lemmatization.
    """
    context = models.CharField(max_length=255, blank=True)
    lemma = models.CharField(max_length=255)
    node = models.ForeignKey(
        LatticeNode,
        related_name="lemma_strings", on_delete=models.CASCADE)

    def __str__(self):
        return self.lemma + " [" + self.context + "]"

    def to_dict(self):
        """
        serialises the node with its form/lemma strings and descendants
        """
        d = {
            "pk": self.pk,
            "lemma": self.lemma,
            "context": self.context,
            "node": self.node.to_dict(),
        }

        return d
