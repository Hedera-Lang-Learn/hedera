#!/usr/bin/env python

import csv

from tqdm import tqdm

from lemmatization.models import LatinLexicon


# Note that latin_lexicon.csv is a SQLite dump:
#   sqlite3 -header -csv LatinMorph16.db "select distinct token, lemma from Lexicon order by token;"
file_path = "import-data/latin_lexicon_frequencies.csv"
total_lines = sum(1 for i in open(file_path, "r"))
print(f"Begin latin lexicon import (size: {total_lines})")

# Bulk import the rows
with open(file_path) as f:
    csv_reader = csv.DictReader(f, delimiter="\t")
    count = 0
    batch_size = 5000
    batch = []
    for row in tqdm(csv_reader, total=total_lines):
        data = dict(token=row["token"], lemma=row["lemma"])
        if row["rank"]:
            data["rank"] = row["rank"]
        if row["count"]:
            data["count"] = row["count"]
        if row["rate"]:
            data["rate"] = row["rate"]

        batch.append(LatinLexicon(**data))
        if len(batch) == batch_size:
            LatinLexicon.objects.bulk_create(batch, batch_size)
            batch = []
            count += batch_size
    if len(batch) > 0:
        LatinLexicon.objects.bulk_create(batch)

print("Completed latin lexicon import.")
