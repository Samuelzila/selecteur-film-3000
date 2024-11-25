import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import json
import os

class Profil(tk.Frame):

    def __init__(self, master=None,fichier_profil="profils.json"):
        super().__init__(master)
        self.master = master
        self.fichier_profil = fichier_profil
        self.liste_profil = self.charger_profils()
        self.create_widgets()

    def create_widgets(self):
        
        self.grid(row=0, column=0, padx=80, pady=20, sticky="nsew")
        
        #Choisir un profil
        n = tk.StringVar()

        #Choix de profil
        self.label_choixprofil = ctk.CTkLabel(self, text="Choisir un profil:", text_color="black")
        self.label_choixprofil.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.choixprofil = ttk.Combobox(self, width=20, textvariable=n)
        self.choixprofil.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.update_combobox()
        self.choixprofil.set("")  # Valeur spar défaut vide

        #Nom
        self.label_nom = ctk.CTkLabel(self, text="Nom:", text_color="black")
        self.label_nom.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.entry_nom = ctk.CTkEntry(self, placeholder_text="unknown")
        self.entry_nom.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        #Email
        self.label_email = ctk.CTkLabel(self, text="Email:", text_color="black")
        self.label_email.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.entry_email = ctk.CTkEntry(self, placeholder_text="unknown")
        self.entry_email.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        #Age
        self.label_age = ctk.CTkLabel(self, text="Age:", text_color="black")
        self.label_age.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.entry_age = ctk.CTkEntry(self, placeholder_text="unknown")
        self.entry_age.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        
        # Bouton pour Créer le profil
        self.créer_le_profil = ctk.CTkButton(self, text="Créer le profil",  command=self.créer_le_profil)
        self.créer_le_profil.grid(row=5, column=1, padx=10, pady=20, sticky="w")
        
        # Bouton pour skip
        self.skip = ctk.CTkButton(self, text="Skip",  command=self.next)
        self.skip.grid(row=5, column=2, padx=10, pady=20, sticky="w")

    #Met à jour les valeurs de la combobox
    def update_combobox(self):
        self.choixprofil["values"] = [profil["nom"] for profil in self.liste_profil]

    # Changer de fenêtre avec skip
    def next(self):
        self.master.show_accueil()

    # Changer de fenêtre avec création de profil
    def créer_le_profil(self):
        
        # Créer une personne à partir des informations fournies
        personne = {"nom" : self.entry_nom.get(), "email" : self.entry_email.get(),"age" : self.entry_age.get()}
        
        # Ajoute la personnee à la liste de profil
        self.liste_profil.append(personne)
        
        # Sauvegarde la liste mise à jour
        self.sauvegarder_profils()
        
        # Met à jour la combobox
        self.update_combobox()

        # Vider les champs après ajout
        self.entry_nom.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)

    def sauvegarder_profils(self):
        """Sauvegarde la liste des profils dans un fichier JSON."""
        with open(self.fichier_profil, "w") as fichier:
            json.dump(self.liste_profil, fichier, indent=4)

    def charger_profils(self):
        """Charge la liste des profils depuis un fichier JSON."""
        if os.path.exists(self.fichier_profil):
            with open(self.fichier_profil, "r") as fichier:
                return json.load(fichier)
        return []

