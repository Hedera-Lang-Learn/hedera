import pandas as pd


"""
Performs 2 outer joins using distinct_lemmas.csv as the base to match against shortdefs.csv and frequencies.csv
Outputs the merged tables into a tsv to migrate into the lemmas table
"""
df1 = pd.read_csv("import-data/distinct_lemmas.csv")
df2 = pd.read_csv("import-data/shortdefs.csv")

# omitted lookupform
df3 = pd.read_csv("import-data/frequencies.csv", usecols=["lemma", "rank", "count", "rate"])

df1["lemma"] = df1["lemma"].str.lower()
df2["lemma"] = df2["lemma"].str.lower()
df4 = pd.merge(df1, df2, on="lemma", how="outer")

df5 = pd.merge(df4, df3, on="lemma", how="outer")
df5.set_index("lemma", inplace=True)
# Replaces the zeros with blanks in the def column
df5["def"].where(df5["def"] == 0, "", inplace=True)

# Combines like rows
g = df5.groupby(by="lemma").agg({"def": "sum", "rank": "first", "count": "first", "rate": "first"})

g.to_csv("distinct_lemma_short_defs_frequencies.tsv", sep="\t")
