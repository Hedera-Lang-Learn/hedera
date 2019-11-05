#!/usr/bin/env python


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


with open("import-data/ivy_lattice.tsv") as f:
    for row in f:
        print(row.strip())
        logeion_lemma, logeion_frequency, morpheus_lemma, sub_lemma, short_def, shorter_def = row.strip().split("|")
        lattice_node, _ = LatticeNode.objects.get_or_create(label=sub_lemma, gloss=shorter_def, canonical=True)
        print("  created lattice_node", lattice_node.pk, sub_lemma, shorter_def)
        create_lemma_node(morpheus_lemma, lattice_node, "morpheus")
        print()
