from django.db import models


class LatticeNode(models.Model):

    label = models.TextField()
    children = models.ManyToManyField("self", symmetrical=False)


def node_info(pk):
    print(pk)
    node = LatticeNode.objects.get(pk=pk)
    if node.form_strings.exists():
        print("forms:")
        for form_node in node.form_strings.all():
            print(f"    - {form_node.form} [{form_node.context}]")
    if node.lemma_strings.exists():
        print("lemmas:")
        for lemma_node in node.lemma_strings.all():
            print(f"    - {lemma_node.lemma} [{lemma_node.context}]")
    if node.glosses.exists():
        print("glosses:")
        for node_gloss in node.glosses.all():
            print(f"    - {node_gloss.gloss}")
    if node.children.exists():
        print("children:")
        for child in node.children.all():
            print(f"    - {child.pk}")


class FormNode(models.Model):
    """
    mapping from form string to lattice node (in a given context)

    This effectively defines a node in a lattice as "meaning" this form.
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
        LatticeNode,
        related_name="form_strings", on_delete=models.CASCADE)


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
