#!/usr/bin/env python
# NOTE: this script is based on load_logeion_lattice.py to do a basic import of russian


from lattices.models import LatticeNode, LemmaNode


def create_lemma_node(lemma, lattice_node, context):
    lemma_node, created = LemmaNode.objects.get_or_create(
        context=context,
        lemma=lemma,
        defaults={
            "node": lattice_node,
        }
    )
    if created:
        print("  created", context, "lemma node", lemma_node.pk, lemma)
    else:
        existing_lattice_node = lemma_node.node
        print(" ", context, "node already existed pointing to lattice node", existing_lattice_node.pk, existing_lattice_node.label)
        if existing_lattice_node.canonical:
            parent_lattice_node = LatticeNode.objects.create(label=lemma, gloss="from " + context, canonical=False)
            parent_lattice_node.children.add(existing_lattice_node)
            parent_lattice_node.children.add(lattice_node)
            parent_lattice_node.save()
            lemma_node.node = parent_lattice_node
            lemma_node.save()
            print("  created parent lattice node", parent_lattice_node.pk, parent_lattice_node.label)
            print("  lattice node", existing_lattice_node.pk, existing_lattice_node.label, "put under", parent_lattice_node.pk, parent_lattice_node.label)
            print("  lattice node", lattice_node.pk, lattice_node.label, "put under", parent_lattice_node.pk, parent_lattice_node.label)
            print(" ", context, "node now points to lattice node", lemma_node.node.pk, lemma_node.node.label)
        else:
            existing_lattice_node.children.add(lattice_node)
            print("  lattice node", lattice_node.pk, lattice_node.label, "put under", existing_lattice_node.pk, existing_lattice_node.label)
            existing_lattice_node.save()


with open("import-data/clancy-russian.tsv") as f:
    for row in f:
        print(row.strip())
        clancy_lemma, short_def = (row.strip().split("\t") + [None, None])[:2]
        if LemmaNode.objects.filter(lemma=clancy_lemma, context="clancy").exists():
            pass
        else:
            lattice_node, _ = LatticeNode.objects.get_or_create(label=clancy_lemma, gloss=short_def or "unglossed", canonical=False)
            print("  created lattice_node", lattice_node.pk, clancy_lemma, short_def)
            create_lemma_node(clancy_lemma, lattice_node, "clancy")
            print()
