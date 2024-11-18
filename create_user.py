import customtkinter as ctk
import os
import json


class CreateUser(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # Groupe pour l'entrée du nom d'utilisateur
        name_group = ctk.CTkFrame(self, fg_color="transparent")
        name_group.place(relx=0.5, rely=0.4, anchor="center")

        name_label = ctk.CTkLabel(name_group, text="Nom d'utilisateur :")
        name_label.pack(side="left")

        self.name_entry = ctk.CTkEntry(name_group)
        self.name_entry.pack()

        # Bouton de soumission
        self.submit_button = ctk.CTkButton(
            self, text="Créer le profil", command=self.submit_form)
        self.submit_button.place(relx=0.5, rely=0.5, anchor="center")

    def submit_form(self):
        nom = self.name_entry.get()

        # Création de l'utilisateur

        # Création d'un dossier d'utilisateurs.
        chemin_dossier = "./users/"
        if not os.path.exists(chemin_dossier):
            os.makedirs(chemin_dossier)

        # Objet utilisateur
        user = {
            "name": nom,
            "blacklist": []
        }

        # Écriture des données dans un fichier
        with open(chemin_dossier+nom+".json", "w", encoding="utf-8") as file:
            file.write(json.dumps(user))

        # Retour à l'accueil
        self.master.show_profiles()
