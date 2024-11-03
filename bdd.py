import pandas as pd
import numpy as np


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


def converter_genres(value):
    """
    Gestion des genres. Convertir le string en array.
    """
    try:
        return value.split(",")
    except (ValueError, TypeError):
        return []


bdd = pd.read_csv("./data/title.basics.tsv",
                  delimiter="\t", converters={"isAdult": converter_bool, "startYear": converter_uint16, "endYear": converter_uint16, "runtimeMinutes": converter_uint16, "genres": converter_genres}, dtype={"tconst": str, "titleType": str, "primaryTitle": str, "originalTitle": str}, usecols=["isAdult", "startYear", "endYear", "genres", "tconst", "titleType", "primaryTitle", "originalTitle", "runtimeMinutes"])

# Ignorer films pour adultes
bdd.drop(bdd[bdd["isAdult"] == True].index, inplace=True)

# Supprimer la colonne maintenant inutile
bdd.drop("isAdult", axis=1, inplace=True)
