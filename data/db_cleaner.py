import pandas as pd

df = pd.read_csv("./title.basics.tsv", delimiter="\t")

# Ignorer films pour adultes
df.drop(df[df["isAdult"] == True].index, inplace=True)

# Garder juste les films
df.drop(df[df["titleType"] != "movie"].index, inplace=True)

df.to_csv("./title.basics.tsv", index=False, sep="\t")

ratings = pd.read_csv("./title.ratings.tsv", sep="\t")

ratings = ratings[ratings["tconst"].isin(df["tconst"])]

ratings.to_csv("./title.ratings.tsv", sep="\t", index=False)
