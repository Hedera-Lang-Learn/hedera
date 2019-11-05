#!/usr/bin/env python


from lattices.models import LatticeNode, LemmaNode


with open("import-data/ivy_lattice.tsv") as f:
    for row in f:
        print(row.strip())
        logeion_lemma, logeion_frequency, morpheus_lemma, sub_lemma, short_def, shorter_def = row.strip().split("|")
        label = sub_lemma + " " + short_def
        lattice_node, _ = LatticeNode.objects.get_or_create(label=label, canonical=True)
        print("  created lattice_node", lattice_node.pk, label)
        morpheus_lemma_node, created = LemmaNode.objects.get_or_create(
            context="morpheus",
            lemma=morpheus_lemma,
            defaults={
                "node": lattice_node,
            }
        )
        if created:
            print("  created morpheus lemma node", morpheus_lemma_node.pk, morpheus_lemma)
        else:
            existing_lattice_node = morpheus_lemma_node.node
            print("  morpheus node already existed pointing to lattice node", existing_lattice_node.pk, existing_lattice_node.label)
            if existing_lattice_node.canonical:
                parent_lattice_node = LatticeNode.objects.create(label="morpheus " + morpheus_lemma, canonical=False)
                parent_lattice_node.children.add(existing_lattice_node)
                parent_lattice_node.children.add(lattice_node)
                parent_lattice_node.save()
                morpheus_lemma_node.node = parent_lattice_node
                morpheus_lemma_node.save()
                print("  created parent lattice node", parent_lattice_node.pk, parent_lattice_node.label)
                print("  lattice node", existing_lattice_node.pk, existing_lattice_node.label, "put under", parent_lattice_node.pk, parent_lattice_node.label)
                print("  lattice node", lattice_node.pk, lattice_node.label, "put under", parent_lattice_node.pk, parent_lattice_node.label)
                print("  morpheus node now points to lattice node", morpheus_lemma_node.node.pk, morpheus_lemma_node.node.label)
            else:
                existing_lattice_node.children.add(lattice_node)
                print("  lattice node", lattice_node.pk, lattice_node.label, "put under", existing_lattice_node.pk, existing_lattice_node.label)
                existing_lattice_node.save()
        print()
