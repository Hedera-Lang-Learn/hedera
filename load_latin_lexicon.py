#!/usr/bin/env python

import csv

from lemmatization.models import LatinLexicon


# Note that latin_lexicon.csv is a SQLite dump:
#   sqlite3 -header -csv LatinMorph16.db "select distinct token, lemma from Lexicon order by token;"
file_path = "import-data/latin_lexicon.csv"
total_lines = sum(1 for i in open(file_path, "r"))

# Bulk import the rows
with open(file_path) as f:
    count = 0
    batch_size = 5000
    batch = []
    for row in csv.DictReader(f, delimiter=","):
        batch.append(LatinLexicon(token=row["token"], lemma=row["lemma"]))
        if len(batch) == batch_size:
            LatinLexicon.objects.bulk_create(batch, batch_size)
            batch = []
            count += batch_size
            print("Latin lexicon import {:.1%}".format(count / total_lines))
    if len(batch) > 0:
        LatinLexicon.objects.bulk_create(batch)
        print("Latin lexicon import completed")
