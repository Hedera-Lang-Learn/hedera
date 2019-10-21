#!/usr/bin/env python

import csv
import unicodedata

from lattices.utils import get_or_create_node_for_lemma
from vocab_list.models import VocabularyList, VocabularyListEntry


def strip_diacritics(s):
    return unicodedata.normalize(
        "NFC",
        "".join((
            c
            for c in unicodedata.normalize("NFD", s)
            if unicodedata.category(c) != "Mn"
        ))
    )

with open("import-data/dcc_latin_morpheus.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)

    vocab_list, created = VocabularyList.objects.get_or_create(
        title = "DCC Latin Core Vocabulary",
        lang = "lat",
        defaults = {
            "description": "The thousand most common words in Latin compiled by a team at Dickinson College led by Christopher Francese."
        },
    )

    for row in reader:
        headword = row[1]
        gloss = row[2]
        morpheus = row[3]

        entry = VocabularyListEntry.objects.create(
            vocabulary_list=vocab_list,
            headword=headword,
            gloss=gloss
        )

    for entry in vocab_list.entries.all():
        if entry.node is None:
            lemma = entry.headword.split()[0].strip(",")
            l1 = get_or_create_node_for_lemma(lemma)
            stripped_lemma = strip_diacritics(lemma)
            if stripped_lemma != lemma:
                l2 = get_or_create_node_for_lemma(stripped_lemma)
                l2.children.add(l1)
            if morpheus and morpheus != lemma and morpheus != stripped_lemma:
                l3 = get_or_create_node_for_lemma(morpheus)
                l3.children.add(l1)

            entry.node = l1
            entry.save()
