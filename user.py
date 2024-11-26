import json
import os


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

    @staticmethod
    def create_user(name):
        """
        Création d'un utilisateur.
        Retourne False en cas d'échec.
        """
        try:
            # Création d'un dossier d'utilisateurs.
            chemin_dossier = "./users/"
            if not os.path.exists(chemin_dossier):
                os.makedirs(chemin_dossier)

            # Objet utilisateur
            user = {
                "name": name,
                "blacklist": []
            }

            # Écriture des données dans un fichier
            with open(chemin_dossier+name+".json", "w", encoding="utf-8") as file:
                file.write(json.dumps(user))

            return True
        except Exception:
            return False

    @staticmethod
    def remove_user(name):
        """
        Supprime un utilisateur.
        Retourne False en cas d'échec.
        """
        try:
            os.remove(f"./users/{name}.json")
            return True
        except Exception:
            return False
