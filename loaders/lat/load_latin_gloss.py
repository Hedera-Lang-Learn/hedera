import csv

from tqdm import tqdm

from lemmatization.models import Gloss, Lemma


file_path = "data/lat/gloss_table.tsv"
total_lines = sum(1 for i in open(file_path, "r"))
print(f"Begin latin gloss import (size: {total_lines})")

with open(file_path) as f:
    csv_reader = csv.DictReader(f, delimiter="\t")
    batch_size = 5000
    batch = []
    all_lemmas_qs = Lemma.objects.all()
    all_gloss_qs = Gloss.objects.all()
    lemmas_data = {q.lemma: q for q in all_lemmas_qs}
    all_gloss_data = {str(g.lemma_id) + g.gloss: g for g in all_gloss_qs}

    for row in tqdm(csv_reader, total=total_lines):
        lemma = row["lemma"]
        gloss = row["gloss"]
        lemma_exist = lemma in lemmas_data
        lemma_object = lemmas_data.get(lemma)
        gloss_exist = False
        if lemma_exist:
            lemma_id = lemma_object.id
            gloss_exist = str(lemma_id) + gloss in all_gloss_data
        if lemma_exist and gloss and not gloss_exist:
            data = dict(gloss=gloss, lemma=lemma_object)
            batch.append(Gloss(**data))
        if len(batch) == batch_size:
            Gloss.objects.bulk_create(batch, batch_size)
            batch = []
    if len(batch) > 0:
        Gloss.objects.bulk_create(batch, batch_size)
