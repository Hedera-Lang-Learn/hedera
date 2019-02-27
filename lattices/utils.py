from .models import FormNode, LatticeNode, LemmaNode


def make_label(kind, value, context):

    if context:
        label = f"{kind} {value} [{context}]"
    else:
        label = f"{kind} {value}"

    return label


def make_lemma(lemma, context=""):

    node_for_lemma = LatticeNode.objects.create(label=make_label("lemma", lemma, context))
    LemmaNode.objects.create(context=context, lemma=lemma, node=node_for_lemma)

    return node_for_lemma


def make_form(form, context=""):

    node_for_form = LatticeNode.objects.create(label=make_label("form", form, context))
    FormNode.objects.create(context=context, form=form, node=node_for_form)

    return node_for_form


def get_or_create_node_for_lemma(lemma, context):

    lemma_node = LemmaNode.objects.filter(context=context, lemma=lemma).first()
    if lemma_node:
        return lemma_node.node
    else:
        return make_lemma(lemma, context)


def get_or_create_node_for_form(form, context):

    form_node = FormNode.objects.filter(context=context, form=form).first()
    if form_node:
        return form_node.node
    else:
        return make_form(form, context)


def foo(form, lemmas, context):

    node_for_form = get_or_create_node_for_form(form, context)

    for lemma in lemmas:
        node_for_form.children.add(get_or_create_node_for_lemma(lemma, context))

    return node_for_form


def get_lattice_node(lemmas, form=None, context=""):
    """
    get or create a LatticeNode from the given lemma(s) (and possibly form)

    LemmaNode(s) (and FormNode) will also be created if necessary.

    `lemmas` can be a string (a single lemma, in which case `form` is ignored)
    or a list of strings (multiple lemmas, in which case `form` is required)
    """

    if not isinstance(lemmas, list):
        lemmas = [lemmas]

    if not lemmas:
        return

    elif len(lemmas) == 1:
        return get_or_create_node_for_lemma(lemmas[0], context)

    else:  # more than one lemma
        if form is None:
            raise ValueError("form cannot be None if more than one lemma")

        return foo(form, lemmas, context)
