import pandas as pd


"""
Performs 3 outer joins using distinct_lemmas.csv as the base to match against shortdefs.csv, frequencies.csv, and ivy_lattice_new
The script will then output the merged tables into a tsv to migrate into the lemmas table
"""
distinct_lemmas = pd.read_csv("merge-data/distinct_lemmas.csv")
short_defs = pd.read_csv("merge-data/shortdefs.csv")

# omitted lookupform column
lemma_frequencies = pd.read_csv("merge-data/frequencies.csv", usecols=["lemma", "rank", "count", "rate"])
ivy_lattice = pd.read_csv("merge-data/ivy_lattice_new.csv", usecols=["lemma", "alt_lemma", "label"])
merge_distinct_lemmas_short_defs = pd.merge(distinct_lemmas, short_defs, on="lemma", how="outer")

merge_lemmas_short_defs_frequencies = pd.merge(merge_distinct_lemmas_short_defs, lemma_frequencies, on="lemma", how="outer")
merge_lemmas_short_defs_frequencies.set_index("lemma", inplace=True)

final_aggregated_lemmas = pd.merge(merge_lemmas_short_defs_frequencies, ivy_lattice, on="lemma", how="outer")

# lowercase capital letters
final_aggregated_lemmas["lemma"] = final_aggregated_lemmas["lemma"].str.lower()

# fill null values with blank
final_aggregated_lemmas[["def"]] = final_aggregated_lemmas[["def"]].fillna("")

# Combines entries with same lemma into single row
grouped_by_lemmas = final_aggregated_lemmas.groupby(by="lemma").agg({"def": "sum", "alt_lemma": "first", "label": "first", "rank": "first", "count": "first", "rate": "first"})

grouped_by_lemmas.to_csv("import-data/distinct_lemma_short_defs_frequencies.tsv", sep="\t")
