import customtkinter as ctk
import os
from functools import partial
import json
import bdd
from user import User


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

        titre_blacklist = ctk.CTkLabel(
            self, text="Liste noire", font=("Arial", 30, "bold"))
        titre_blacklist.pack()

        # Grille pour les entrées de la blacklist
        grid = ctk.CTkFrame(self, fg_color="transparent")
        # Pour chaque film dans la blacklist, on crée une entrée pour le supprimer.
        for i, idfilm in enumerate(blacklist):
            # Ajout d'un bouton carré, pour supprimer
            label = ctk.CTkLabel(grid, text=bdd.get_title(idfilm))
            label.grid(column=0, row=i, pady=20, sticky="w", padx=10)
            delete_button = ctk.CTkButton(
                grid, text="×", command=partial(self.remove_from_blacklist, idfilm), width=30, height=30, font=("Arial", 20, "bold"), fg_color="#af0000")
            delete_button.grid(column=1, row=i)
        grid.pack()

        # Bouton pour changer d'utilisateur
        delete_user = ctk.CTkButton(
            self.master, text="Changer d'utilisateur", command=self.master.show_profiles)
        delete_user.place(anchor="se", relx=1-20/self.master.winfo_width(),
                          rely=1-70/self.master.winfo_height())

        # Bouton pour supprimmer l'utilisateur
        delete_user = ctk.CTkButton(
            self.master, text="Supprimer l'utilisateur", command=self.remove_user, fg_color="#af0000")
        delete_user.place(anchor="se", relx=1-20/self.master.winfo_width(),
                          rely=1-30/self.master.winfo_height())

    def remove_from_blacklist(self, idfilm):
        self.master.user.remove_from_blacklist(idfilm)
        self.master.show_blacklist()

    def remove_user(self):
        User.remove_user(self.master.user.name)
        self.master.user = None
        self.master.show_profiles()
