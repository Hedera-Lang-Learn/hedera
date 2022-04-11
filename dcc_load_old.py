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

with open("import-data/dcc_latin_old.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)

    vocab_list, created = VocabularyList.objects.get_or_create(
        title = "DCC Latin Core Vocabulary",
        lang = "lat",
        defaults = {
            "description": "The thousand most common words in Latin compiled by a team at Dickinson College led by Christopher Francese."
        },
    )

    for row in reader:
        headword, gloss = row[:2]

        entry = VocabularyListEntry.objects.create(
            vocabulary_list=vocab_list,
            headword=headword,
            gloss=gloss
        )

    for entry in vocab_list.entries.all():
        if entry.node is None:
            lemma = entry.headword.split()[0]
            l1 = get_or_create_node_for_lemma(lemma) # TODO: replace with LemmaNode.objects.filter(...)
            stripped_lemma = strip_diacritics(lemma)
            if stripped_lemma != lemma:
                l2 = get_or_create_node_for_lemma(stripped_lemma)
                l2.children.add(l1)
            entry.node = l1
            entry.save()
