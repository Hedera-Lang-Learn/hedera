import csv

from tqdm import tqdm

from lemmatization.models import Gloss, Lemma


file_path = "import-data/distinct_lemma_short_defs_frequencies.tsv"
total_lines = sum(1 for i in open(file_path, "r"))
print(f"Begin latin gloss import (size: {total_lines})")

with open(file_path) as f:
    csv_reader = csv.DictReader(f, delimiter="\t")
    batch_size = 5000
    batch = []
    all_lemmas_qs = Lemma.objects.all()
    all_gloss_qs = Gloss.objects.all()
    for row in tqdm(csv_reader, total=total_lines):
        lemma = row["lemma"]
        gloss = row["def"]
        lemma_exist = all_lemmas_qs.filter(lemma=lemma).first()
        gloss_exist = all_gloss_qs.filter(gloss=gloss, lemma=lemma_exist).first()
        if lemma_exist and gloss and not gloss_exist:
            data = dict(gloss=gloss, lemma=lemma_exist)
            batch.append(Gloss(**data))
        if len(batch) == batch_size:
            Gloss.objects.bulk_create(batch, batch_size)
            batch = []
    if len(batch) > 0:
        Gloss.objects.bulk_create(batch, batch_size)
