import sys

import pandas as pd


try:
    filename = sys.argv[1]
    filename_base = filename[:-4]
except IndexError:
    print("Must include target file location")
    exit()

df = pd.read_csv(filename, sep="\t")

chapters = df.chapter.unique()
chapters.sort()
chapters = [int(chapter) for chapter in chapters]
digits = len(str(max(chapters)))
outputformat = f"{{filename_base}}_ch{{c:0{digits}}}.tsv"

for c in chapters:
    df[df.chapter <= c].to_csv(
        outputformat.format(filename_base=filename_base, c=c),
        sep="\t"
    )
