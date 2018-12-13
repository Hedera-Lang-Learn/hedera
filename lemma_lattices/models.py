from django.db import models


class LemmaLatticeNode(models.Model):

    children = models.ManyToManyField("self", symmetrical=False)


class FormNode(models.Model):
    """
    mapping from form string to lemma lattice node (in a given context)

    This effectively defines a node in a lemma lattice as "meaning" this form.
    Note that not all forms should be mapped in this way, only those that have
    their own node in the lattice (for example, because their ambiguous).  If
    the form string is ambiguous, the referenced node can have a child for each
    possibility.

    The "context" is just an optional label to clarify interpretation if a
    form coming from one place should be treated differently from one coming
    from another place.
    """
    context = models.CharField(max_length=255, blank=True)
    form = models.CharField(max_length=255)
    node = models.ForeignKey(
        LemmaLatticeNode,
        related_name="form_strings", on_delete=models.CASCADE)


class LemmaNode(models.Model):
    """
    mapping from lemma string to lemma lattice node (in a given context)

    This effectively defines a node in a lemma lattice as "meaning" anything
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
        LemmaLatticeNode,
        related_name="lemma_strings", on_delete=models.CASCADE)


class NodeGloss(models.Model):
    """
    a human-readable gloss for a particular lattice node

    May not be a "gloss" in the traditional sense but just some text that
    helps indicate what a node "means". For example, the node representing
    an ambiguous "est" might just be glossed "ambiguous est" or similar.
    """
    node = models.ForeignKey(
        LemmaLatticeNode, related_name="glosses", on_delete=models.CASCADE)
    gloss = models.TextField()
