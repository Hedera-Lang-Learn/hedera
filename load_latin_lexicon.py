#!/usr/bin/env python

import csv

from tqdm import tqdm

from lemmatization.services.latin import LatinLexicon


"""
This script imports the frequency data from latin_lexicon_frequencies.csv into the lemmatizaion_lexicon table
Notes:
    - Changed batch size to 1000 because of "psycopg2.OperationalError: server closed the connection unexpectedly"
    - Used dict data structure for faster data import(about 8mins or so for 506,092 entries)
Example data:
data from the parsed csv: [{'token': 'Aecum', 'lemma': 'aequus'}, ...]

existing_ids_token data dict: {'ABACTVSabigo':(7,"ABACTVS","abigo"), ...}
    Stucture of the data dict is {token+lemma:(id, token, lemma)}
"""
# Note that latin_lexicon.csv is a SQLite dump:
#   sqlite3 -header -csv LatinMorph16.db "select distinct token, lemma from Lexicon order by token;"
file_path = "import-data/latin_lexicon_frequencies.csv"
total_lines = sum(1 for i in open(file_path, "r"))
print(f"Begin latin lexicon import (size: {total_lines})")

# Bulk import the rows
with open(file_path) as f:
    csv_reader = csv.DictReader(f, delimiter="\t")
    update_count = 0
    create_count = 0
    batch_size = 1000
    create_batch = []
    update_batch = []
    existing_ids_token = {lt[1] + lt[2]: lt for lt in LatinLexicon.objects.all().values_list("id", "token", "lemma")}
    for row in tqdm(csv_reader, total=total_lines):
        data = dict(token=row["token"], lemma=row["lemma"])
        if row["rank"]:
            data["rank"] = row["rank"]
        if row["count"]:
            data["count"] = row["count"]
        if row["rate"]:
            data["rate"] = row["rate"]
        # check if token already exist in the table
        exists = existing_ids_token[row["token"] + row["lemma"]]
        if exists:
            id, _, _ = exists
            data["id"] = id
            update_batch.append(LatinLexicon(**data))
        else:
            create_batch.append(LatinLexicon(**data))
        if len(create_batch) == batch_size:
            LatinLexicon.objects.bulk_create(create_batch, batch_size)
            create_batch = []
            create_count += batch_size
        if len(update_batch) == batch_size:
            LatinLexicon.objects.bulk_update(update_batch, ["count", "rank", "rate"], batch_size)
            update_batch = []
            update_count += batch_size

    if len(create_batch) > 0:
        LatinLexicon.objects.bulk_create(create_batch)
    if len(update_batch) > 0:
        LatinLexicon.objects.bulk_update(update_batch, ["count", "rank", "rate"])

print("Completed latin lexicon import.")
