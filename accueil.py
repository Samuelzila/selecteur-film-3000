import random
import json
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import bdd as BDD
from bdd import bdd
from bdd import genres
import datetime
import pandas as pd
from functools import partial


class Accueil(ctk.CTkFrame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.liste_genres = []

    # Fonctions qui assurent que les recherches sont valides -----------------------------

    def range_annee(self, entry):
        if int(entry) < 1900 or int(entry) > datetime.datetime.now().year + 5:
            return True

    def genres_exist(self, entry):
        if entry not in genres:
            return True
        else:
            return False

    def range_rating(self, entry):
        if int(entry) < 0 or int(entry) > 10:
            return True

    def cohérence_rating(self, entry1, entry2):
        if entry1 >= entry2:
            return True
        else:
            return False

    def cohérence_annee(self, entry1, entry2):
        if entry1 >= entry2:
            return True
        else:
            return False

    def is_empty(self, entry, entry2, entry3, entry4, entry5):
        if entry == "" or entry2 == "" or entry3 == "" or entry4 == "":
            return True
    # donne du feedback en cas d'erreur

    def show_invalid_entry(self):
        ctk.CTkLabel(self, text="Veuillez entrer des valeurs valides.", text_color="red").grid(
            row=4, column=0, padx=10, pady=10, sticky="w")

        cohérence_annees = self.cohérence_annee(
            int(self.entry_annee_max.get()), int(self.entry_annee_min.get()))
        cohérence_rating = self.cohérence_rating(
            int(self.entry_rating_max.get()), int(self.entry_rating_min.get()))
        genres_not_exist = self.genres_exist(self.choixGenre.get())

        if not self.range_annee(self.entry_annee_max.get()) and cohérence_annees:
            self.entry_annee_max.configure(text_color="green")
        else:
            self.entry_annee_max.configure(text_color="red")

        if not self.range_annee(self.entry_annee_min.get()) and cohérence_annees:
            self.entry_annee_min.configure(text_color="green")
        else:
            self.entry_annee_min.configure(text_color="red")

        if not self.range_rating(self.entry_rating_max.get()) and cohérence_rating:
            self.entry_rating_max.configure(text_color="green")
        else:
            self.entry_rating_max.configure(text_color="red")

        if not self.range_rating(self.entry_rating_min.get()) and cohérence_rating:
            self.entry_rating_min.configure(text_color="green")
        else:
            self.entry_rating_min.configure(text_color="red")

    # --------------------------------------------------------------
    def collect_info(self):

        # Vérification des informations entrées
        if self.is_empty(self.entry_annee_max.get(), self.entry_annee_min.get(), self.entry_rating_max.get(), self.entry_rating_min.get(), self.liste_genres):
            ctk.CTkLabel(self, text="Veuillez entrer des valeurs.", text_color="red").grid(
                row=4, column=0, padx=10, pady=10, sticky="w")
        else:
            # vérification des informations valides
            if self.range_annee(self.entry_annee_max.get()) or self.range_annee(self.entry_annee_min.get()) or self.range_rating(self.entry_rating_max.get()) or self.range_rating(self.entry_rating_min.get()) or not self.cohérence_rating(int(self.entry_rating_max.get()), int(self.entry_rating_min.get())) or not self.cohérence_annee(int(self.entry_annee_max.get()), int(self.entry_annee_min.get())):
                self.show_invalid_entry()
            else:
                # Collecte des informations entrées par l'utilisateur
                annee_max = self.entry_annee_max.get()
                annee_min = self.entry_annee_min.get()
                rating_max = self.entry_rating_max.get()
                rating_min = self.entry_rating_min.get()
                genre = self.liste_genres

                # Changer de fenêtre
                self.master.show_Films(
                    tuple(self.Resultat(annee_max, annee_min, rating_max, rating_min, genre)))

    def Resultat(self, annee_max, annee_min, rating_max, rating_min, desired_genres):
        # Recherche des films parmi la base de données

        blacklist = self.master.user.blacklist

        if len(desired_genres) == 0:
            data = bdd[(bdd["startYear"] >= int(annee_min)) & (
                bdd["startYear"] <= int(annee_max)) & (bdd["averageRating"] <= int(rating_max)) & (bdd["averageRating"] >= int(rating_min)) & ~bdd.index.isin(blacklist)]

        else:
            data = bdd[(bdd["genres"].apply(lambda x: any(genre in x for genre in desired_genres))) & (bdd["startYear"] >= int(annee_min)) & (
                bdd["startYear"] <= int(annee_max)) & (bdd["averageRating"] <= int(rating_max)) & (bdd["averageRating"] >= int(rating_min)) & ~bdd.index.isin(blacklist)]

        # si la recherche ne renvoie pas 3 films, on ajoute des films au hasard dans la liste filtrée, jusqu'à ce qu'elle contienne 3
        if len(data.index) < 3:
            data = pd.concat([data, bdd.sample(3-len(data.index))])

        # si la recherche renvoie plus de 3 films, on ajoute des films au hasard depuis la recherche
        return data.sample(3).index

    def refresh_genres(self):
        """
        Met à jour les genres sélectionnés dans l'interface graphique.
        """
        for child in self.liste_genres_frame.winfo_children():
            child.destroy()
        for i, genre in enumerate(self.liste_genres):
            label = ctk.CTkLabel(self.liste_genres_frame,
                                 text=BDD.genre_decode(genre))
            label.grid(row=i, column=0, pady=5, padx=10, sticky="w")
            # Supprimer une sélection en cliquant dessus.
            label.bind("<Button-1>", partial(self.remove_genre, genre))

    def add_genres(self):
        """
        Ajoute un genre à la liste parmis laquelle on fait le filtre.
        """

        genre = self.choixGenre.get()
        if self.genres_exist(genre) or BDD.genre_encode(genre) in self.liste_genres:
            self.choixGenre.configure(foreground="red")
        else:
            self.choixGenre.configure(foreground="green")
            self.liste_genres.append(BDD.genre_encode(self.choixGenre.get()))
            self.choixGenre.set("")

        # Mettre à jour l'interface graphique
        self.refresh_genres()

    def remove_genre(self, genre, event):
        """
        Retire un genre de la liste des genres sélectionnés
        """
        self.liste_genres.remove(genre)
        # Mettre à jour l'interface
        self.refresh_genres()

    def refresh_year_sliders(self, value):
        """
        Met à jour les nombres pour les sliders d'année, et synchronise les extremums.
        """
        # S'assurer que le minimum est inférieur au max et vice-versa
        if value < self.entry_annee_min.get():
            self.entry_annee_min.set(value)
        elif value > self.entry_annee_max.get():
            self.entry_annee_max.set(value)

        # Mettre à jour les labels
        self.label_annee_max.configure(
            text=f"Année maximale: {self.entry_annee_max.get():.0f}")
        self.label_annee_min.configure(
            text=f"Année minimale: {self.entry_annee_min.get():.0f}")

    def refresh_rating_sliders(self, value):
        """
        Met à jour les nombres pour les sliders de score, et synchronise les extremums.
        """
        # S'assurer que le minimum est inférieur au max et vice-versa
        if value < self.entry_rating_min.get():
            self.entry_rating_min.set(value)
        elif value > self.entry_rating_max.get():
            self.entry_rating_max.set(value)

        # Mettre à jour les labels
        self.label_rating_max.configure(
            text=f"Score maximal: {self.entry_rating_max.get():.1f}")
        self.label_rating_min.configure(
            text=f"Score minimal: {self.entry_rating_min.get():.1f}")

    def create_widgets(self):

        # Définir la liste des genres avant de l'utiliser
        liste_des_genres = list(genres.value_to_key.keys())

        # Variable pour stocker la sélection
        genre_input = tk.StringVar()

        # Frame pour contenir le formulaire
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.place(anchor="n", relx=.5, rely=.2)

        # Création de labels et entrées pour les années
        self.label_annee_max = ctk.CTkLabel(
            form_frame, text=f"Année maximale: {datetime.datetime.now().year}")
        self.label_annee_max.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_annee_max = ctk.CTkSlider(
            form_frame, from_=1900, to=datetime.datetime.now().year, command=self.refresh_year_sliders)
        self.entry_annee_max.set(datetime.datetime.now().year)
        self.entry_annee_max.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_annee_min = ctk.CTkLabel(
            form_frame, text="Année minimale: 1900")
        self.label_annee_min.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.entry_annee_min = ctk.CTkSlider(
            form_frame, from_=1900, to=datetime.datetime.now().year, command=self.refresh_year_sliders)
        self.entry_annee_min.set(1900)
        self.entry_annee_min.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Création de labels et entrées pour les Rating
        self.label_rating_max = ctk.CTkLabel(
            form_frame, text="Score maximal: 10.0")
        self.label_rating_max.grid(
            row=1, column=3, padx=10, pady=5, sticky="w")

        self.entry_rating_max = ctk.CTkSlider(
            form_frame, from_=0, to=10, command=self.refresh_rating_sliders)
        self.entry_rating_max.set(10)
        self.entry_rating_max.grid(
            row=1, column=4, padx=10, pady=5, sticky="w")

        self.label_rating_min = ctk.CTkLabel(
            form_frame, text="Score minimal: 0.0")
        self.label_rating_min.grid(
            row=2, column=3, padx=10, pady=5, sticky="w")

        self.entry_rating_min = ctk.CTkSlider(
            form_frame, from_=0, to=10, command=self.refresh_rating_sliders)
        self.entry_rating_min.set(0)
        self.entry_rating_min.grid(
            row=2, column=4, padx=10, pady=5, sticky="w")

        # Bouton pour collecter les informations
        self.collect_button = ctk.CTkButton(
            form_frame, text="Envoyer",  command=self.collect_info)
        self.collect_button.grid(row=3, column=4, padx=10, pady=20, sticky="e")

        # Gérer les genres
        self.add_Genre = ctk.CTkButton(form_frame, text="ajouter Genre",  command=self.add_genres,
                                       fg_color="gray", text_color="white", hover_color="black")
        self.add_Genre.grid(row=3, column=1, padx=10, pady=20, sticky="w")

        # Création du combobox avec la liste des genres
        self.choixGenre = ttk.Combobox(
            form_frame, width=20, textvariable=genre_input)
        self.choixGenre.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.choixGenre["values"] = liste_des_genres
        self.choixGenre.set("")  # Valeur spar défaut vide

        # Fonction de recherche pour filtrer les options en fonction de la saisie
        def recherche_Liste(event):

            value = event.widget.get()
            if value == "":
                self.choixGenre["values"] = liste_des_genres
            else:
                # Filtrer les mois en fonction de la saisie
                data = [item for item in liste_des_genres if value.lower()
                        in item.lower()]
                self.choixGenre["values"] = data

        # Associer la fonction de recherche au combobox
        self.choixGenre.bind("<KeyRelease>", recherche_Liste)

        # Configuration des colonnes pour s'assurer que chaque colonne a une taille uniforme
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")

        # Afficher une liste des genres séléctionnés
        self.liste_genres_frame = ctk.CTkFrame(
            form_frame, fg_color="transparent")
        self.liste_genres_frame.grid(
            row=4, column=0, pady=5, padx=10, sticky="nw")

        # Bouton de gestion de profil
        user_button = ctk.CTkButton(
            self, height=30, width=30, text=self.master.user.initials, command=self.master.show_blacklist)
        user_button.place(
            anchor="ne", relx=1-20/self.master.winfo_width(), rely=20/self.master.winfo_height())
