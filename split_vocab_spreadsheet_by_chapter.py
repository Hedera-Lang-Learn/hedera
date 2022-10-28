import sys

import pandas as pd


try:
    filename = sys.argv[1]
    filename_base = filename[:-4]
except IndexError:
    print("Must include target file location")
    exit()

df = pd.read_csv(filename, sep="\t")

if "chapter" not in df.columns:
    print("Spreadsheet must include a 'chapter' column")
    exit()

# Get unique chapters in a list as ints
chapters = df.chapter.unique()
chapters.sort()
chapters = [int(chapter) for chapter in chapters]

# Get the max number of digits in chapters, so they can be numbered like "01"
# or "028" as needed
digits = len(str(max(chapters)))

# Make an output format template with the number of digits calculated above
outputformat = f"{{filename_base}}_ch{{c:0{digits}}}.tsv"

# Output a new spreadsheet for each chapter. The list should include the
# chapter in the filename, as well as all lower-numbered chapters. The
# filenames will be formatted like {filename_base}_ch{chapter_number}.tsv,
# where chapter_numbers are left-padded with zeros up to the maximum number of
# digits in the list of unique chapters.
for c in chapters:
    df[df.chapter <= c].to_csv(
        outputformat.format(filename_base=filename_base, c=c),
        sep="\t"
    )
