#!/usr/bin/env python
# NOTE: this script is based on load_clancy_lattice.py to do a basic import of Chinese dictionary data
import re
import time
from typing import Optional, Tuple

from lattices.models import LatticeNode, LemmaNode


DICT_FILE = "import-data/cedict_ts.u8"
DEFAULT_LEMMA_NODE_CONTEXT = "chinese"


def create_lemma_node(lemma, lattice_node, context=DEFAULT_LEMMA_NODE_CONTEXT):
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


def get_or_create_lattice_node(label: str, gloss) -> Tuple[Optional[LemmaNode], bool]:
    return LatticeNode.objects.get_or_create(label=label, gloss=gloss, canonical=False)


def node_exists(lemma: str) -> bool:
    return LemmaNode.objects.filter(lemma=lemma, context=DEFAULT_LEMMA_NODE_CONTEXT).exists()


row_grouping_re = re.compile(r"^(?P<lemma>\S+) (?P<altform>\S+) (?P<defn>.*)$")

ROW_COUNT_FOR_UPDATE = 100
ROW_TO_START_FROM = 1  # set this higher e.g. to resume from a previous point
current_row = 0
start_time = time.time()
block_start_time = start_time
rows = []

with open(DICT_FILE) as f:
    rows = f.readlines()

for row in rows:
    current_row += 1

    # skip the first `ROW_TO_START_FROM` rows so we can
    # resume from a previous run
    if current_row < ROW_TO_START_FROM:
        continue

    if current_row % ROW_COUNT_FOR_UPDATE == 0:
        current_time = time.time()
        block_time = round(current_time - block_start_time, 2)
        print("Processing row", current_row, f"(last block of rows took {block_time}s)", flush=True)
        block_start_time = current_time

    clean_row = row.strip()
    if clean_row.startswith("#") or clean_row == "":
        # this isn't a row we care about
        continue

    matches = row_grouping_re.match(clean_row)
    if not matches:
        print("Error: format not recognized for line", clean_row)
        continue
    dictionary_lemma = matches["lemma"]
    alternate_form = matches["altform"]
    short_def = matches["defn"]
    full_def = f"{dictionary_lemma} {alternate_form} {short_def or 'unglossed'}"

    # although redundant to check for existence before running get_or_create,
    # checking for existence is much faster so leads to speed-ups when records
    # already exist in the DB
    if not node_exists(dictionary_lemma):
        lattice_node, created = get_or_create_lattice_node(dictionary_lemma, full_def)
        create_lemma_node(dictionary_lemma, lattice_node)

    # we also want to ensure that a headword with a different alternate form (i.e.
    # for which the simplified form is different from the traditional form) can be
    # found for glosses also
    if dictionary_lemma != alternate_form and not node_exists(alternate_form):
        lattice_node, created = get_or_create_lattice_node(alternate_form, full_def)
        create_lemma_node(alternate_form, lattice_node)

end_time = time.time()

print("Processed", current_row, "rows in", end_time - start_time, "seconds")
