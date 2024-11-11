import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import bdd as BDD
from bdd import bdd
from bdd import genres
import datetime

import json
import random


class Accueil(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.liste_genres = []

    # Fonctions qui assure que les recherches sont valides -----------------------------

    def range_annee(self, entry):
        if not entry.isdigit():
            return True
        if int(entry) < 1900 or int(entry) > datetime.datetime.now().year + 5:
            return True

    def genres_exist(self, entry):
        if entry not in genres:
            return True
        else:
            return False

    def range_rating(self, entry):
        if not entry.isdigit():
            return True
        if int(entry) < 0 or int(entry) > 10:
            return True

    def cohérence_rating(self, entry1, entry2):
        if entry1 >= entry2:
            print(entry1, entry2)
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
        print(cohérence_annees)
        cohérence_rating = self.cohérence_rating(
            int(self.entry_rating_max.get()), int(self.entry_rating_min.get()))
        print(cohérence_rating)
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

        if len(desired_genres) == 0:
            data = bdd[(bdd["startYear"] >= int(annee_min)) & (
                bdd["startYear"] <= int(annee_max)) & (bdd["averageRating"] <= int(rating_max)) & (bdd["averageRating"] >= int(rating_min))]

        else:
            data = bdd[(bdd["genres"].apply(lambda x: any(genre in x for genre in desired_genres))) & (bdd["startYear"] >= int(annee_min)) & (
                bdd["startYear"] <= int(annee_max)) & (bdd["averageRating"] <= int(rating_max)) & (bdd["averageRating"] >= int(rating_min))]

        try:
            with open("data/blacklist.json") as file:

                blacklist = json.load(file)
        except FileNotFoundError:
            blacklist = []

        liste_des_films = []
        nombre_de_film = 3

        # si la recherche ne renvoie pas 3 films, on ajoute des films au hasard
        if len(data) < 3:
            nombre_de_film = len(data)
            print("nombre de film : ", nombre_de_film)
            for i in range(0, 3 - nombre_de_film):
                trouver = False
                while (not trouver):
                    idFilm = bdd.sample(
                        1, random_state=random.randint(0, 10000)).index[0]

                    if idFilm not in blacklist:
                        blacklist.append(idFilm)
                        liste_des_films.append(idFilm)
                        trouver = True

        # si la recherche renvoie plus de 3 films, on ajoute des films au hasard depuis la recherche
        print(nombre_de_film)
        for i in range(0, nombre_de_film):
            while (True):
                idFilm = data.sample(1).index[0]
                if idFilm not in blacklist:
                    break
            blacklist.append(idFilm)
            liste_des_films.append(idFilm)

        return liste_des_films

    def add_genres(self):

        if self.genres_exist(self.choixGenre.get()):
            print("mauvaise entrée")
            self.choixGenre.configure(foreground="red")
        else:
            self.choixGenre.configure(foreground="green")
            self.liste_genres.append(BDD.genre_encode(self.choixGenre.get()))
            print(self.choixGenre.get())
            print(BDD.genre_encode(self.choixGenre.get()))
            print(self.liste_genres)
            self.choixGenre.set("")

    # visuel de la recherhe
    def create_widgets(self):
        self.grid(row=0, column=0, padx=80, pady=20, sticky="nsew")

        # Définir la liste des genres avant de l'utiliser
        liste_des_genres = list(genres.value_to_key.keys())

        # Variable pour stocker la sélection
        n = tk.StringVar()

        # Création de labels et entrées pour les années
        self.label_annee_max = ctk.CTkLabel(
            self, text="Année Max:", text_color="black")
        self.label_annee_max.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_annee_max = ctk.CTkEntry(self, placeholder_text="2000")
        self.entry_annee_max.insert(0, f"{datetime.datetime.now().year}")
        self.entry_annee_max.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_annee_min = ctk.CTkLabel(
            self, text="Année Min:", text_color="black")
        self.label_annee_min.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.entry_annee_min = ctk.CTkEntry(self, placeholder_text="2000")
        self.entry_annee_min.insert(0, "1900")
        self.entry_annee_min.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Création de labels et entrées pour les Rating
        self.label_rating_max = ctk.CTkLabel(
            self, text="Rating Max:", text_color="black")
        self.label_rating_max.grid(
            row=1, column=3, padx=10, pady=5, sticky="w")

        self.entry_rating_max = ctk.CTkEntry(
            self, placeholder_text="10")
        self.entry_rating_max.insert(0, "10")
        self.entry_rating_max.grid(
            row=1, column=4, padx=10, pady=5, sticky="w")

        self.label_rating_min = ctk.CTkLabel(
            self, text="Rating Min:", text_color="black")
        self.label_rating_min.grid(
            row=2, column=3, padx=10, pady=5, sticky="w")

        self.entry_rating_min = ctk.CTkEntry(self, placeholder_text="0")
        self.entry_rating_min.insert(0, "0")
        self.entry_rating_min.grid(
            row=2, column=4, padx=10, pady=5, sticky="w")

        # Bouton pour collecter les informations
        self.collect_button = ctk.CTkButton(
            self, text="Collecter",  command=self.collect_info)
        self.collect_button.grid(row=3, column=3, padx=10, pady=20, sticky="w")

        self.add_Genre = ctk.CTkButton(self, text="ajouter Genre",  command=self.add_genres,
                                       fg_color="gray", text_color="white", hover_color="black")
        self.add_Genre.grid(row=3, column=1, padx=10, pady=20, sticky="w")

        # Création du combobox avec la liste des genres
        self.choixGenre = ttk.Combobox(self, width=20, textvariable=n)
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
