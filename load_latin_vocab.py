#!/usr/bin/env python

"""
This script imports core/system vocabulary lists for latin.

Usage:
    python manage.py shell -c "import load_latin_vocab"
"""

import csv

from vocab_list.models import VocabularyList, VocabularyListEntry


CORE_VOCAB_LISTS = [
    {
        "filename": "shelmerdine.csv",
        "title": "Shelmerdine 2nd Edition Vocabulary",
        "description": "Vocabulary from the 2nd Edition of Susan Shelmerdine's Introduction to Latin",
        "fieldnames": ["headword", "chapter", "definition"],
    },
    {
        "filename": "dcc_latin_morpheus.csv",
        "title": "DCC Latin Core Vocabulary",
        "description": "The thousand most common words in Latin compiled by a team at Dickinson College led by Christopher Francese.",
        "fieldnames": ["frequency_rank", "headword", "definition"],
    },
]

for core_vocab in CORE_VOCAB_LISTS:
    filename = core_vocab["filename"]
    title = core_vocab["title"]
    description = core_vocab["description"]
    fieldnames = core_vocab["fieldnames"]

    with open(f"import-data/{filename}", newline="") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        vocab_list, vocab_list_created = VocabularyList.objects.get_or_create(
            title=title,
            lang="lat",
            description=description,
        )

        for row in reader:
            entry, entry_created = VocabularyListEntry.objects.get_or_create(
                vocabulary_list=vocab_list,
                headword=row["headword"],
                definition=row["definition"]
            )
