import csv

from tqdm import tqdm

from lemmatization.models import Lemma


file_path = "import-data/lemma_frequency.tsv"
total_lines = sum(1 for i in open(file_path, "r"))
print(f"Begin latin lemma import (size: {total_lines})")

with open(file_path) as f:
    csv_reader = csv.DictReader(f, delimiter="\t")

    count_1 = 0
    batch_size = 2
    batch = []
    all_lemmas_qs = Lemma.objects.values()
    lemmas_data = {q["lemma"]: q for q in all_lemmas_qs}

    for row in tqdm(csv_reader, total=total_lines):
        count_1 += 1
        val = list(row.values())
        lemma, alt_lemma, label, short_def, rank, count, rate = val

        data = dict(lang="lat", lemma=lemma.lower())

        lemma_exist = lemmas_data.get(lemma)
        if alt_lemma:
            data["alt_lemma"] = alt_lemma.lower()
        else:
            data["alt_lemma"] = lemma.lower()
        if label:
            data["label"] = label.lower()
        else:
            data["label"] = lemma.lower()
        if rank:
            data["rank"] = float(rank)
        else:
            data["rank"] = 99999
        if count:
            data["count"] = float(count)
        else:
            data["count"] = 0
        if rate:
            data["rate"] = float(rate)
        else:
            data["rate"] = 0.000
        if not label:
            data["label"] = lemma.lower()
        if not lemma_exist and lemma:
            batch.append(Lemma(**data))

        if len(batch) == batch_size:
            Lemma.objects.bulk_create(batch, batch_size)
            batch = []
            count_1 = batch_size
    if len(batch) > 0:
        Lemma.objects.bulk_create(batch, batch_size)
