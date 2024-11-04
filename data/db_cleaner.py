import pandas as pd

df = pd.read_csv("./title.basics.tsv", delimiter="\t")

# Ignorer films pour adultes
df.drop(df[df["isAdult"] == True].index, inplace=True)

# Garder juste les films
df.drop(df[df["titleType"] != "movie"].index, inplace=True)

# Supprimer la colonne maintenant inutile
df.drop("titleType", axis=1, inplace=True)

df.to_csv("./title.basics.tsv", index=False, sep="\t")
