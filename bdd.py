import pandas as pd
import numpy as np
from double_dictionary import DoubleDict


def converter_uint16(value):
    """
    Gestion des nombres durant la lecture de la bdd.
    """
    try:
        return np.uint16(value)
    except (ValueError, TypeError):
        return np.nan  # Replace bad data with NaN


def converter_bool(value):
    """
    Gestion des booléens durant la lecture de la bdd.
    """
    try:
        return True if value == "1" else False
    except (ValueError, TypeError):
        return False


# Un ensemble de genres, ce qui permettera d'encoder les genres de la bdd et sauver de la mémoire.
# Ne pas jouer avec directement. Utiliser les fonction associées.
genres = DoubleDict()


def genre_encode(genre):
    if genre in genres:
        return genres.get_key(genre)
    else:
        key = np.uint8(len(genres))
        genres.insert(key, genre)
        return key


def genre_decode(genre):
    if genre in genres:
        return genres.get(genre)
    else:
        raise ValueError("This encoded value has no associated genre.")


def converter_genres(value):
    """
    Gestion des genres. Convertir le string en array.
    """
    try:
        arr = value.split(",")
        encoded_arr = []
        for i in arr:
            if i == "\\N":
                continue
            encoded_arr.append(genre_encode(i))
        return encoded_arr

    except (ValueError, TypeError):
        return []


bdd = pd.read_csv("./data/title.basics.tsv",
                  delimiter="\t", converters={"isAdult": converter_bool, "startYear": converter_uint16, "endYear": converter_uint16, "runtimeMinutes": converter_uint16, "genres": converter_genres}, dtype={"tconst": str, "titleType": str, "primaryTitle": str, "originalTitle": str}, usecols=["isAdult", "startYear", "endYear", "genres", "tconst", "titleType", "primaryTitle", "originalTitle", "runtimeMinutes"], index_col="tconst")

# Ignorer films pour adultes
bdd.drop(bdd[bdd["isAdult"] == True].index, inplace=True)

# Supprimer la colonne maintenant inutile
bdd.drop("isAdult", axis=1, inplace=True)
mem = bdd.memory_usage(deep=True)
print(mem)
print(f"Sum: {mem.sum():_}")
