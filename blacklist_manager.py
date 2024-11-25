import customtkinter as ctk
import os
from functools import partial
import json
import bdd


class BlacklistManager(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.create_widgets()

    def create_widgets(self):
        blacklist = self.master.user.blacklist

        # Bouton de retour
        retour = ctk.CTkButton(
            self, text="←", command=self.master.show_accueil, height=30, width=30)
        retour.place(anchor="nw", relx=20/self.master.winfo_width(),
                     rely=20/self.master.winfo_height())

        # Pour chaque film dans la blacklist, on crée une entrée pour le supprimer.
        for idfilm in blacklist:
            # Groupe pour les éléments d'une entrée
            label_group = ctk.CTkFrame(self, fg_color="transparent")
            # Ajout d'un bouton carré, pour le profil
            label = ctk.CTkLabel(label_group, text=bdd.get_title(idfilm))
            label.pack(side="left")
            delete_button = ctk.CTkButton(
                label_group, text="×", command=partial(self.remove_from_blacklist, idfilm), width=30, height=30, font=("Arial", 20, "bold"), fg_color="red")
            delete_button.pack(padx=10)
            label_group.pack(pady=10)

        # Bouton pour changer d'utilisateur
        create_user = ctk.CTkButton(
            self.master, text="Créer un profil", command=self.master.show_create_user)
        create_user.place(relx=0.5, rely=0.5, anchor="center")

    def remove_from_blacklist(self, idfilm):
        self.master.user.remove_from_blacklist(idfilm)
        self.master.show_blacklist()
