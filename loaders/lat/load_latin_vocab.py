#!/usr/bin/env python

"""
This script imports core/system vocabulary lists for latin.

Usage:
    python manage.py shell -c "import loaders.lat.load_latin_vocab"
"""

import csv

from tqdm import tqdm

from lemmatized_text.models import Lemma
from vocab_list.models import VocabularyList, VocabularyListEntry


SYSTEM_VOCAB_LISTS = [
    {
        "filename": "shelmerdine_latin.tsv",
        "title": "Shelmerdine 2nd Edition Vocabulary",
        "description": "Vocabulary from the 2nd Edition of Susan Shelmerdine's Introduction to Latin",
    },
    {
        "filename": "dcc_latin_morpheus.tsv",
        "title": "DCC Latin Core Vocabulary",
        "description": "The thousand most common words in Latin compiled by a team at Dickinson College led by Christopher Francese. See http://dcc.dickinson.edu/vocab/core-vocabulary",
    },
]

for system_vocab in SYSTEM_VOCAB_LISTS:
    filename = system_vocab["filename"]
    filepath = f"data/lat/vocab/{filename}"
    title = system_vocab["title"]
    description = system_vocab["description"]

    total_lines = sum(1 for i in open(filepath, "r"))
    print(f"Begin vocab list import {filename} (size: {total_lines})")

    with open(filepath, newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter="\t")
        has_lemma_field = csv_reader.fieldnames and "lemma" in csv_reader.fieldnames

        vocab_list, vocab_list_created = VocabularyList.objects.get_or_create(
            title=title,
            lang="lat",
            defaults={"description": description},
        )

        for row in tqdm(csv_reader, total=total_lines):
            entry = dict(
                vocabulary_list=vocab_list,
                headword=row["headword"],
                definition=row["definition"],
            )

            # Try to link to the lemma directly if it is specified in the vocab list,
            # otherwise a link job will try to do this automatically.
            if has_lemma_field and row["lemma"]:
                try:
                    entry["lemma"] = Lemma.objects.get(lemma=row["lemma"])
                except Lemma.DoesNotExist:
                    print(f"Lemma does not exist: {row}")

            entry, entry_created = VocabularyListEntry.objects.get_or_create(**entry)
