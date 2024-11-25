import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import bdd as BDD
from bdd import bdd
from bdd import genres
import datetime
from CTkListbox import *
import json
import random
from ttkwidgets import TickScale

#TODO: ajouter sélection biaisé 
#TODO: ajouter genre sélectif

#ajout de CTkFrame pour changer l'apparance
BACKGROUND_COLOR = "#2b2b2b"

BUTTON_COLOR = "#FCC398"
BUTTON_TEXT_COLOR = "#2b2b2b"
BUTTON_COLOR_HOVER = "#DFAD86"

COLOR_RED = "#FC707A"
HOVER_COLOR_RED = "#DF626B"

COLOR_BLUE = "#47A4AF"
HOVER_COLOR_BLUE = "#3C8A93"

COLOR_WHITE = "#ffffff"
HOVER_COLOR_WHITE = "#E2E2E2"
class Accueil(ctk.CTkFrame):

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
        
        # Collecte des informations entrées par l'utilisateur
        annee_max = self.max_slider.get()
        annee_min = self.min_slider.get()
        rating_max = self.max_slider_rating.get()/10
        rating_min = self.min_slider_rating.get()/10
        duration_max = self.max_slider_temps.get()
        duration_min = self.min_slider_temps.get()
        print("duration max : ", duration_max, "duration min : ", duration_min)
        genre = self.liste_genres      
         # Changer de fenêtre
        self.master.show_Films(tuple(self.Resultat(annee_max, annee_min, rating_max, rating_min, genre, duration_max, duration_min)))

    def Resultat(self, annee_max, annee_min, rating_max, rating_min, desired_genres, duration_max, duration_min):
        # Recherche des films parmi la base de données

        #genre vide
        if len(desired_genres) == 0:
            data = bdd[(bdd["startYear"] >= int(annee_min)) & (
                bdd["startYear"] <= int(annee_max)) & (bdd["averageRating"] <= int(rating_max)) & (bdd["averageRating"] >= int(rating_min))& (bdd["averageRating"] >= int(rating_min)) & (bdd["runtimeMinutes"] <= int(duration_max)) & (bdd["runtimeMinutes"] >= int(duration_min))]

        else:
            print(" duration max : ",int(duration_max), int(duration_min))
            data = bdd[(bdd["genres"].apply(lambda x: any(genre in x for genre in desired_genres))) & (bdd["startYear"] >= int(annee_min))
                        & (bdd["startYear"] <= int(annee_max)) & (bdd["averageRating"] <= int(rating_max)) & (bdd["averageRating"] >= int(rating_min)) & (bdd["runtimeMinutes"] <= int(duration_max)) & (bdd["runtimeMinutes"] >= int(duration_min))]

        try:
            with open("data/blacklist.json") as file:

                blacklist = json.load(file)
        except FileNotFoundError:
            blacklist = []
        
        print(data["runtimeMinutes"])

        liste_des_films = []
        rating_liste = []
        nombre_de_film = 3

        # si la recherche ne renvoie pas 3 films, on ajoute des films au hasard
        if len(data) < 3:
            nombre_de_film = len(data)
            print("nombre de film : ", nombre_de_film)
            for i in range(0, 3 - nombre_de_film):
                trouver = False
                while (not trouver):
                    idFilm = bdd.sample(1, random_state=random.randint(0, 10000)).index[0]

                    if idFilm not in blacklist:
                        blacklist.append(idFilm)
                        liste_des_films.append(idFilm)
                        trouver = True

        # si la recherche renvoie plus de 3 films, on ajoute des films au hasard depuis la recherche
        if len(data) > nombre_de_film*3:
            print(nombre_de_film)
            for i in range(0, nombre_de_film*3):
                while (True):
                    idFilm = data.sample(1)
                    rating_liste.append([idFilm["averageRating"].values[0], idFilm.index[0]])
                    if idFilm not in blacklist:
                        break
            print(rating_liste)
            rating_liste.sort(reverse=True)
            print(rating_liste)
            for i in range(0, 3):
                liste_des_films.append(rating_liste[i][1])
                print(liste_des_films)
                blacklist.append(rating_liste[i][1])
        
        else:
            print(nombre_de_film)
            for i in range(0, nombre_de_film*10):
                while (True):
                    idFilm = data.sample(1).index[0]
                    if idFilm not in blacklist:
                        break
                blacklist.append(idFilm)
                liste_des_films.append(idFilm)
        
        return liste_des_films

    def add_genres(self):

        if self.genres_exist(self.choixGenre.get() or self.choixGenre.get() in self.liste_genres):
            print("mauvaise entrée")
            self.choixGenre.configure(foreground="red")
        else:
            self.choixGenre.configure(foreground="green")
            self.liste_genres.append(BDD.genre_encode(self.choixGenre.get()))
            print(self.choixGenre.get())
            print(BDD.genre_encode(self.choixGenre.get()))
            print(self.liste_genres)
            self.ajout_de_genre.insert(ctk.END, self.choixGenre.get())
            self.choixGenre.set("")
            self.supprimer_genre_button.insert(ctk.END, "X")
            #self.entry_genre.delete(0, tk.END)

    # visuel de la recherhe

    
    def create_widgets(self):

    # Bouton pour afficher la valeur actuelle
        ctk.set_appearance_mode("dark")
        self.grid(row=0, column=0, padx=80, pady=20, sticky="nsew")

        # Définir la liste des genres avant de l'utiliser
        liste_des_genres = list(genres.value_to_key.keys())

        # Variable pour stocker la sélection
        n = tk.StringVar()
        n = liste_des_genres
        ###################################################################################################
        # Labels


        # Titre
        self.Titre = ctk.CTkLabel(self, text="Sélecteur-Film-3000", text_color="white", font=("Arial", 30, "bold"), justify="center")
        self.Titre.place(relx=0.5, rely=0.05, anchor="center")

        # Plage années
        self.range_label = ctk.CTkLabel(self, text="Années min: 1900 -  Années max: 2024", text_color=COLOR_WHITE, font=("Arial", 14))
        self.range_label.place(relx=0.1, rely=0.2, anchor="w")

        self.min_slider = ctk.CTkSlider(self, from_=1900, to=datetime.datetime.now().year, command=self.update_range, progress_color=COLOR_BLUE, button_color= COLOR_WHITE,button_hover_color = HOVER_COLOR_WHITE)
        self.min_slider.set(1900)
        self.min_slider.place(relx=0.1, rely=0.25, relwidth=0.3)

        self.max_slider = ctk.CTkSlider(self, from_=1900, to=datetime.datetime.now().year, command=self.update_range,progress_color=COLOR_BLUE, button_color= COLOR_WHITE, button_hover_color = HOVER_COLOR_WHITE)
        self.max_slider.set(datetime.datetime.now().year)
        self.max_slider.place(relx=0.1, rely=0.3, relwidth=0.3)


        # Plage ratings
        self.range_label_rating = ctk.CTkLabel(self, text="Rating min: 0  -  Rating max: 10", text_color=COLOR_WHITE, font=("Arial", 14))
        self.range_label_rating.place(relx=0.6, rely=0.2, anchor="w")

        self.min_slider_rating = ctk.CTkSlider(self, from_=0, to=100, command=self.update_range_rating,progress_color=COLOR_BLUE, button_color= COLOR_WHITE,  button_hover_color = HOVER_COLOR_WHITE)
        self.min_slider_rating.set(0)
        self.min_slider_rating.place(relx=0.6, rely=0.25, relwidth=0.3)

        self.max_slider_rating = ctk.CTkSlider(self, from_=0, to=100, command=self.update_range_rating,progress_color=COLOR_BLUE, button_color= COLOR_WHITE,  button_hover_color = HOVER_COLOR_WHITE)
        self.max_slider_rating.set(100)
        self.max_slider_rating.place(relx=0.6, rely=0.3, relwidth=0.3)

        # Plage Temps des films:

        self.range_label_temps = ctk.CTkLabel(self, text="Duration min: 0  -  Duration max: 180", text_color=COLOR_WHITE, font=("Arial", 14))
        self.range_label_temps.place(relx=0.6, rely=0.4, anchor="w")

        self.min_slider_temps = ctk.CTkSlider(self, from_=0, to=180, command=self.update_range_Temps,progress_color=COLOR_BLUE, button_color= COLOR_WHITE,  button_hover_color = HOVER_COLOR_WHITE, )
        self.min_slider_temps.set(0)
        self.min_slider_temps.place(relx=0.6, rely=0.45, relwidth=0.3)

        self.max_slider_temps = ctk.CTkSlider(self, from_=0, to=180, command=self.update_range_Temps,progress_color=COLOR_BLUE, button_color= COLOR_WHITE,  button_hover_color = HOVER_COLOR_WHITE)
        self.max_slider_temps.set(180)
        self.max_slider_temps.place(relx=0.6, rely=0.50, relwidth=0.3)       
        # Boutons et listes déroulantes
        self.collect_button = ctk.CTkButton(self, text="Collecter", command=self.collect_info, font=("Arial", 14),fg_color=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR, hover_color= BUTTON_COLOR_HOVER ,width=60, height=60, corner_radius=32)
        self.collect_button.place(relx=0.6, rely=0.6, relwidth=0.3)

        self.add_Genre = ctk.CTkButton(self, text="+", command=self.add_genres, fg_color=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR, hover_color= BUTTON_COLOR_HOVER ,width=25, height=25, corner_radius=15, font=("Arial", 12))
        self.add_Genre.place(relx=0.40, rely=0.40, anchor="center")

        self.choixGenre = ttk.Combobox(self, width=19, font=("Arial", 12), justify="center", values=n)
        self.choixGenre.place(relx=0.23, rely=0.40, anchor="center")
        self.choixGenre.set("")

        # Liste des genres ajoutés
        self.ajout_de_genre = CTkListbox(
            self,
            width=210,
            height=200,
            multiple_selection=True,
            border_width=0,
            button_color= COLOR_BLUE,
            hover_color= HOVER_COLOR_BLUE,
            text_color=COLOR_WHITE,
            fg_color="transparent",
            justify="left"
        )
        self.ajout_de_genre.place(relx=0.25, rely=0.6, anchor="center")

        # Bouton pour supprimer un genre
        self.supprimer_genre_button = CTkListbox(
            self,
            command=self.supprimer_genre,
            multiple_selection=True,
            width=30,
            height=200,
            button_color=COLOR_RED,
            hover_color=HOVER_COLOR_RED,
            text_color= COLOR_WHITE,
            border_width=0,
            fg_color="transparent",
            justify="left",
            #scrollbar_button_color="#4f574f"
        )
        self.supprimer_genre_button.place(relx=0.40, rely=0.6, anchor="center")


    

        # Supprimer bouton (placeholder exemple)
        
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

    
    def update_label(self, value):
        """
        Met à jour le label lorsque le slider change.
        """
        self.value_label.configure(text=f"Valeur: {int(float(value))}")

    def display_value(self):
        """
        Affiche la valeur actuelle du slider dans la console.
        """
        print(f"Valeur actuelle: {int(self.slider.get())}") 

    def update_range(self, value):
        
        min_val = int(self.min_slider.get())
        max_val = int(self.max_slider.get())
        # Empêcher que min dépasse max
        if min_val >= max_val:
            self.min_slider.set(max_val - 1)
        # Empêcher que max soit inférieur à min
        if max_val <= min_val:
            self.max_slider.set(min_val + 1)
        self.range_label.configure(text=f"Années min: {int(self.min_slider.get())} -  Années max: {int(self.max_slider.get())}")

    def display_range(self):
        """
        Affiche la plage actuelle dans la console.
        """
        min_val = int(self.min_slider.get())
        max_val = int(self.max_slider.get())
        print(f"Plage actuelle: {min_val} - {max_val}")   
   
    
    def update_range_rating(self, value):
        min_val = int(self.min_slider_rating.get())
        max_val = int(self.max_slider_rating.get())
        # Empêcher que min spepasse max
        if min_val >= max_val:
            self.min_slider_rating.set(max_val - 1)
        # Empêcher que max soit infériror à min
        if max_val <= min_val:
            self.max_slider_rating.set(min_val + 1)
        mi = round(int(self.min_slider_rating.get())*0.1,1)
        ma = round(int(self.max_slider_rating.get())*0.1,1)
        
        print(mi,ma)
        self.range_label_rating.configure(text=f"Rating min: {mi} -  Rating max: {ma}")

    def update_range_Temps(self, value):
        min_val = int(self.min_slider_temps.get())
        max_val = int(self.max_slider_temps.get())
        # Empêcher que min spepasse max
        if min_val >= max_val:
            self.min_slider_temps.set(max_val - 1)
        # Empêcher que max soit infériror à min
        if max_val <= min_val:
            self.max_slider_temps.set(min_val + 1)
        self.range_label_temps.configure(text=f"Duration min: {int(self.min_slider_temps.get())} -  Duration max: {int(self.max_slider_temps.get())}")


    def supprimer_genre(self, val):
        selection = self.supprimer_genre_button.curselection()
        if selection:
            index = selection[0]
            value = self.ajout_de_genre.get(index)
            print("liste des genres", self.liste_genres)
            print("value to remove", value)
            print("decoded value", BDD.genre_encode(value))
            self.ajout_de_genre.delete(index)
            decoded_value = BDD.genre_encode(value)
            if decoded_value in self.liste_genres:
                print("decoded value found in liste_genres")
                self.liste_genres.remove(decoded_value)
            else:
                print("decoded value not found in liste_genres")
            self.supprimer_genre_button.delete(index)
            print("liste des genres", self.liste_genres)  # delete the last item
            #Bug mais ça marche lol