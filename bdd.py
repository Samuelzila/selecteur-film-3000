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

# Garder juste les films
bdd.drop(bdd[bdd["titleType"] != "movie"].index, inplace=True)

# Supprimer la colonne maintenant inutile
bdd.drop("titleType", axis=1, inplace=True)

# Ajout des scores de films
ratings = pd.read_csv("./data/title.ratings.tsv", sep="\t", index_col="tconst",
                      usecols=["tconst", "averageRating"], dtype={"averageRating": np.float16, "tconst": str})

# À ce stade-ci, c'est moins grave de ne pas faire les opérations inplace, car on a moins de films.
bdd = bdd.join(ratings)

del ratings


def get_title(tconst):
    """
    Obtenir le titre d'un film à partir de son identifiant IMDb.
    """
    global bdd
    title = bdd.at[tconst, "primaryTitle"]
    return title


def get_originaltitle(tconst):
    """
    Obtenir le titre original d'un film à partir de son identifiant IMDb.
    """
    global bdd
    return bdd.at[tconst, "originalTitle"]


def get_startYear(tconst):
    """
    Obtenir l'année de départ d'un film à partir de son identifiant IMDb.
    """
    global bdd
    if not np.isnan(bdd.at[tconst, "startYear"]):
        return int(bdd.at[tconst, "startYear"])
    else:
        return np.nan


def get_endYear(tconst):
    """
    Obtenir l'année de fin d'un film à partir de son identifiant IMDb.
    """
    global bdd
    if not np.isnan(bdd.at[tconst, "endYear"]):
        return int(bdd.at[tconst, "endYear"])
    else:
        return np.nan


def get_runtime(tconst):
    """
    Obtenir la durée d'un film à partir de son identifiant IMDb.
    """
    global bdd
    return bdd.at[tconst, "runtimeMinutes"]


def get_genres(tconst):
    """
    Obtenir le genre d'un film à partir de son identifiant IMDb.
    """
    global bdd
    genres = bdd.at[tconst, "genres"]
    liste = []
    for i in genres:
        liste.append(genre_decode(i))
    return liste


def get_rating(tconst):
    """
    Obtenir le score d'un film à partir de son identifiant IMDb.
    """
    global bdd
    return bdd.at[tconst, "averageRating"]
