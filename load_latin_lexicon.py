#!/usr/bin/env python

import csv

from tqdm import tqdm

from lattices.models import LemmaNode
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
    update_lemma_count = 0
    create_count = 0
    batch_size = 1000
    create_batch = []
    # TODO: Add logic to add lemma if does not exist - issues with adding a lattice node due to some lemmas does not have a corresponding lattice node
    # create_lemma_batch = []
    # create_lemma_count = 0
    update_batch = []
    update_lemma_batch = []
    existing_ids_token = {lt[1] + lt[2]: lt for lt in LatinLexicon.objects.all().values_list("id", "token", "lemma")}
    existing_token_lemma = {lemma[0]: lemma for lemma in LemmaNode.objects.all().filter(lang="lat").values_list("id", "lemma")}
    for row in tqdm(csv_reader, total=total_lines):
        data = dict(token=row["token"], lemma=row["lemma"])
        freq_data_lemma = dict(lemma=row["lemma"], rank=99999, count=0, rate=0)
        if row["rank"]:
            data["rank"] = row["rank"]
            freq_data_lemma["rank"] = row["rank"]
        if row["count"]:
            data["count"] = row["count"]
            freq_data_lemma["count"] = row["count"]
        if row["rate"]:
            freq_data_lemma["rate"] = row["rate"]
            data["rate"] = row["rate"]
        # check if token already exist in the table
        exists = existing_ids_token.get(row["token"] + row["lemma"], None)
        exists_in_lemma = existing_token_lemma.get(row["lemma"], None)
        if exists_in_lemma:
            lemma_id, _, _ = exists_in_lemma
            freq_data_lemma["id"] = lemma_id
            update_lemma_batch.append(LemmaNode(**freq_data_lemma))
        # else:
        #     find_lattice_node = [lattice for lattice in LatticeNode.objects.all().filter(label=row["lemma"]).values_list("id", flat=True)]
        #     freq_data_lemma["lang"] = "lat"
        #     # selecting the first ID found - TODO how are we linking LatticeNodes to LemmaNodes
        #     freq_data_lemma["node_id"] = find_lattice_node[0]
        #     create_lemma_batch.append(LemmaNode(**freq_data_lemma))
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
        # if len(create_lemma_batch) == batch_size:
        #     LemmaNode.objects.bulk_create(create_lemma_batch)
        #     create_lemma_batch = []
        #     create_lemma_count += batch_size
            # print('len(create_lemma_batch)= ', len(create_lemma_batch))
        if len(update_lemma_batch) == batch_size:
            LemmaNode.objects.bulk_update(update_lemma_batch, ["count", "rank", "rate"], batch_size)
            update_lemma_batch = []
            update_lemma_count += batch_size

    # print('len(update_lemma_batch)= ', len(update_lemma_batch))
    if len(create_batch) > 0:
        LatinLexicon.objects.bulk_create(create_batch)
    if len(update_batch) > 0:
        LatinLexicon.objects.bulk_update(update_batch, ["count", "rank", "rate"])
    # if len(create_lemma_batch) > 0:
    #     LemmaNode.objects.bulk_create(create_lemma_batch)
    if len(update_lemma_batch) > 0:
        LemmaNode.objects.bulk_update(update_lemma_batch, ["count", "rank", "rate"], batch_size)

print("Completed latin lexicon import.")
