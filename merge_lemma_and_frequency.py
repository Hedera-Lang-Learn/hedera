import pandas as pd


"""
Performs 3 outer joins using distinct_lemmas.csv as the base to match against shortdefs.csv, frequencies.csv, and ivy_lattice_new
The script will then output the merged tables into a tsv to migrate into the lemmas table

Input files:
    - shortdefs.csv: this file is an export of the shortdefs table from morph16.db which contains lemma definitions
    - ivy_lattice_new.csv: this file is manually curated by Ivy Livingston and converted from a tsv file in import-data folder
    - distinct_lemmas.csv: this file is a list created by Bill Barthelmy which contains unique lemmas
    - frequencies.csv: this file is an export of the latininfo.db. This table contains frequency(rank, count, rate) data on different lemmas
 Output file(located in the import-data folder):
   - distinct_lemma_short_defs_frequencies.tsv: merged frequencies, short definitions, and ivy's curated lemmas into a single table of lemmas, which will be used to import into the lemmas table
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
final_aggregated_lemmas.lemma = final_aggregated_lemmas.lemma.str.lower()

# fill null values with blank
final_aggregated_lemmas["def"] = final_aggregated_lemmas["def"].fillna("")

# Combines entries with same lemma into single row
grouped_by_lemmas = final_aggregated_lemmas.groupby(by="lemma").agg({"def": "sum", "alt_lemma": "first", "label": "first", "rank": "first", "count": "first", "rate": "first"})

grouped_by_lemmas.to_csv("import-data/distinct_lemma_short_defs_frequencies.tsv", sep="\t")
