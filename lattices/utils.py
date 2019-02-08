from .models import FormNode, LatticeNode, LemmaNode


def make_label(kind, value, context):

    if context:
        label = f"{kind} {value} [{context}]"
    else:
        label = f"{kind} {value}"

    return label


def get_lattice_node(form, lemmas, context=""):

    if not lemmas:
        return

    elif len(lemmas) == 1:
        lemma = lemmas[0]
        lemma_node = LemmaNode.objects.filter(context=context, lemma=lemma).first()
        if lemma_node:
            return lemma_node.node
        else:
            node = LatticeNode.objects.create(label=make_label("lemma", lemma, context))
            LemmaNode.objects.create(context=context, lemma=lemma, node=node)
            return node

    else:  # more than one lemma
        form_node = FormNode.objects.filter(context=context, form=form).first()
        if form_node:
            node = form_node.node
            for lemma in lemmas:
                lemma_node = LemmaNode.objects.filter(context=context, lemma=lemma).first()
                if lemma_node:
                    node_for_lemma = lemma_node.node
                    if node_for_lemma not in node.children.all():  # check descendants?
                        node.children.add(node_for_lemma)
                else:
                    node_for_lemma = LatticeNode.objects.create(label=make_label("lemma", lemma, context))
                    LemmaNode.objects.create(context=context, lemma=lemma, node=node_for_lemma)
                    node.children.add(node_for_lemma)
            return node
        else:
            node = LatticeNode.objects.create(label=make_label("form", form, context))
            FormNode.objects.create(context=context, form=form, node=node)
            for lemma in lemmas:
                lemma_node = LemmaNode.objects.filter(context=context, lemma=lemma).first()
                if lemma_node:
                    node_for_lemma = lemma_node.node
                    node.children.add(node_for_lemma)
                else:
                    node_for_lemma = LatticeNode.objects.create(label=make_label("lemma", lemma, context))
                    LemmaNode.objects.create(context=context, lemma=lemma, node=node_for_lemma)
                    node.children.add(node_for_lemma)
            return node