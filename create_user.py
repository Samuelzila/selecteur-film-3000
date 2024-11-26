import customtkinter as ctk
import os
import json
from user import User


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
        User.create_user(nom)

        # Retour à l'accueil
        self.master.show_profiles()
