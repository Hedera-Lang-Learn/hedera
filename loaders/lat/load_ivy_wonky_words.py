#!/usr/bin/env python

from lemmatization.models import add_form


with open("import-data/wonky.tsv") as f:
    for row in f:
        form, lemma_list = row.strip().split("\t")
        lemmas = lemma_list.split(",")
        add_form("morpheus", "lat", form, lemmas)
        print(form, lemmas)
