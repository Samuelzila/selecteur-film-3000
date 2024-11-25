import json


class User:
    def __init__(self, name):
        self.name = name
        # Les initiales de l'utilisateur.
        self.initials = "".join([s[0] for s in name.split(" ")])
        self.blacklist = self.load_blacklist()

    def load_blacklist(self):
        """
        Charge la blacklist de l'utilisateur et la retourne dans une liste
        """
        try:
            with open(f"./users/{self.name}.json", "r") as file:
                blacklist = json.load(file)["blacklist"]
        except FileNotFoundError:
            blacklist = []

        return blacklist

    def get_json(self):
        """
        Retourne les données de l'utilisateur en tant que dictionnaire.
        """
        with open(f"./users/{self.name}.json", "r") as file:
            return json.load(file)

    def remove_from_blacklist(self, idfilm):
        """
        Retire un film de la blacklist
        """
        blacklist = self.blacklist
        blacklist.remove(idfilm)

        data = self.get_json()

        data["blacklist"] = blacklist

        self.update(data)

    def add_to_blacklist(self, idfilms):
        """
        Ajouter un film dans la blacklist.
        """
        data = self.get_json()

        self.blacklist.append(idfilms)
        data["blacklist"] = self.blacklist

        self.update(data)

    def update(self, data):
        """
        Prend en entrée un dictionnaire avec un format valide et écrase les données actuelles de l'utilisateur dans le fichier.
        Retourne False s'il y a eu une erreur.
        """
        try:
            with open(f"./users/{self.name}.json", "w") as file:
                file.write(json.dumps(data))
            return True
        except Exception:
            return False
