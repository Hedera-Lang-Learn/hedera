import csv

from tqdm import tqdm

from lemmatization.models import FormToLemma, Lemma


file_path = "data/lat/form_to_lemma_table.tsv"

total_lines = sum(1 for i in open(file_path, "r"))
print(f"Begin latin formtolemma import (size: {total_lines})")

with open(file_path) as f:
    csv_reader = csv.DictReader(f, delimiter="\t")
    all_lemmas_qs = Lemma.objects.all()
    lemmas_data = {q.lemma: q for q in all_lemmas_qs}
    batch_size = 5000
    batch = []
    all_formtolemma_qs = FormToLemma.objects.values()
    formtolemma_data = {q["form"]: q for q in all_formtolemma_qs}
    for row in tqdm(csv_reader, total=total_lines):
        val = list(row.values())
        form, lemma = val
        lemma = lemmas_data.get(lemma)
        form_exist = formtolemma_data.get(form)
        # only adds to the batch if formtolemma does not already exist in the database
        if lemma and not form_exist:
            data = dict(form=form, lemma=lemma, lemma_id=lemma.id, lang="lat")
            batch.append(FormToLemma(**data))
        if len(batch) == batch_size:
            FormToLemma.objects.bulk_create(batch, batch_size)
            batch = []
    if len(batch) > 0:
        FormToLemma.objects.bulk_create(batch, batch_size)
