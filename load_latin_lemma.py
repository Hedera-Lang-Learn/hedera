import csv

from tqdm import tqdm

from lemmatization.models import Lemma


file_path = "import-data/distinct_lemma_short_defs_frequencies.tsv"
total_lines = sum(1 for i in open(file_path, "r"))
print(f"Begin latin lemma import (size: {total_lines})")

with open(file_path) as f:
    csv_reader = csv.DictReader(f, delimiter="\t")
    count = 0
    batch_size = 5000
    batch = []
    all_lemmas_qs = Lemma.objects.values()
    lemmas_data = {q["lemma"]: q for q in all_lemmas_qs}
    for row in tqdm(csv_reader, total=total_lines):
        lemma = row["lemma"]
        alt_lemma = row["alt_lemma"]
        label = row["label"]
        rank = row["rank"]
        count = row["count"]
        rate = row["rate"]
        data = dict(lang="lat", lemma=lemma.lower())
        lemma_exist = lemmas_data.get(lemma)

        # only adds to the batch lemma does not already exist in the database
        if not lemma_exist and lemma:
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
            batch.append(Lemma(**data))

        if len(batch) == batch_size:
            Lemma.objects.bulk_create(batch, batch_size)
            batch = []
            count += batch_size
    if len(batch) > 0:
        Lemma.objects.bulk_create(batch, batch_size)
