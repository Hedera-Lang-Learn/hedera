#!/usr/bin/env python

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


def make_entries_and_nodes(vocab_list, vocab_file):
    for row in vocab_file:
        headword, gloss = row.strip().split("|")

        entry = VocabularyListEntry.objects.create(
            vocabulary_list=vocab_list,
            headword=headword,
            gloss=gloss
        )

    c = vocab_list.entries.count()
    i = 0
    for entry in vocab_list.entries.all():
        i += 1
        print(i, c)
        if entry.node is None:
            lemma = entry.headword.split()[0]
            l1 = get_or_create_node_for_lemma(lemma)
            stripped_lemma = strip_diacritics(lemma)
            if stripped_lemma != lemma:
                l2 = get_or_create_node_for_lemma(stripped_lemma)
                l2.children.add(l1)
            entry.node = l1
            entry.save()


with open("import-data/logeion-greek.txt") as f:

    vocab_list, created = VocabularyList.objects.get_or_create(
        title = "Logeion Greek",
        lang = "grc",
        defaults = {
            "description": "Greek shortdefs from Logeion"
        },
    )

    make_entries_and_nodes(vocab_list, f)


with open("import-data/logeion-latin.txt") as f:

    vocab_list, created = VocabularyList.objects.get_or_create(
        title = "Logeion Latin",
        lang = "lat",
        defaults = {
            "description": "Latin shortdefs from Logeion"
        },
    )

    make_entries_and_nodes(vocab_list, f)
