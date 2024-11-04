class DoubleDict:
    """
    Les dictionnaires sont très efficaces pour l'accès à partir d'une clef. (Vraiment) Pas autant pour l'accès à partir d'une valeur.
    Cette classe vise à corriger se problème en accélérant la vitesse d'accès dans les deux sens, à deux conditions.
    Premièrement, les valeurs doivent être uniques.
    Deuxièmement, on double l'espace en mémoire.
    """

    def __init__(self):
        self.key_to_value = {}
        self.value_to_key = {}

    def insert(self, key, value):
        """
        Insertion d'une valeur dans le dictionnaire.
        Retourne un tuple (clef, valeur).
        """
        if key in self.key_to_value or value in self.value_to_key:
            raise ValueError("Keys and values must be unique")
        self.key_to_value[key] = value
        self.value_to_key[value] = key
        return (key, value)

    def get_key(self, value):
        """
        Retourne la clef à partir de la valeur.
        """
        return self.value_to_key.get(value)

    def get(self, key):
        """
        Retourne la valeur à partir de la clef.
        """
        return self.key_to_value.get(key)

    def remove(self, key):
        """
        Enlève une valeur du dictionnaire.
        """
        if key in self.key_to_value:
            value = self.key_to_value.pop(key)
            self.value_to_key.pop(value)

    def remove_by_value(self, value):
        """
        Enlève une valeur du dictionnaire à partir de la valeur.
        """
        if value in self.value_to_key:
            key = self.value_to_key.pop(value)
            self.key_to_value.pop(key)

    def __len__(self):
        return len(self.key_to_value)

    def __contains__(self, item):
        return item in self.key_to_value or item in self.value_to_key
