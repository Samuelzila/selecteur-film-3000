import pandas as pd

df = pd.read_csv("./title.basics.tsv", delimiter="\t")

# Ignorer films pour adultes
df.drop(df[df["isAdult"] == True].index, inplace=True)

df.to_csv("./title.basics.tsv", index=False, sep="\t")
