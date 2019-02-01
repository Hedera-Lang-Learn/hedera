from .models import FormNode, LatticeNode, LemmaNode, NodeGloss


def make_gloss(kind, value, context):

    if context:
        gloss = f"{kind} {value} [{context}]"
    else:
        gloss = f"{kind} {value}"

    return gloss


def get_lattice_node(form, lemmas, context=""):

    if not lemmas:
        return

    elif len(lemmas) == 1:
        lemma = lemmas[0]
        lemma_node = LemmaNode.objects.filter(context=context, lemma=lemma).first()
        if lemma_node:
            return lemma_node.node
        else:
            node = LatticeNode.objects.create()
            LemmaNode.objects.create(context=context, lemma=lemma, node=node)
            NodeGloss.objects.create(node=node, gloss=make_gloss("lemma", lemma, context))
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
                    node_for_lemma = LatticeNode.objects.create()
                    LemmaNode.objects.create(context=context, lemma=lemma, node=node_for_lemma)
                    NodeGloss.objects.create(node=node_for_lemma, gloss=make_gloss("lemma", lemma, context))
                    node.children.add(node_for_lemma)
            return node
        else:
            node = LatticeNode.objects.create()
            FormNode.objects.create(context=context, form=form, node=node)
            NodeGloss.objects.create(node=node, gloss=make_gloss("form", form, context))
            for lemma in lemmas:
                lemma_node = LemmaNode.objects.filter(context=context, lemma=lemma).first()
                if lemma_node:
                    node_for_lemma = lemma_node.node
                    node.children.add(node_for_lemma)
                else:
                    node_for_lemma = LatticeNode.objects.create()
                    LemmaNode.objects.create(context=context, lemma=lemma, node=node_for_lemma)
                    NodeGloss.objects.create(node=node_for_lemma, gloss=make_gloss("lemma", lemma, context))
                    node.children.add(node_for_lemma)
            return node
