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

#
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
        
    

    ########## RECHERCHE ###############
    def collect_info(self):
        
        # Collecte des informations entrées par l'utilisateur
        annee_max = self.max_slider.get()
        annee_min = self.min_slider.get()
        rating_max = self.max_slider_rating.get()/10 #dvisier par 10 car le slider est sur 100 et le rating sur 10
        rating_min = self.min_slider_rating.get()/10
        duration_max = self.max_slider_temps.get()
        duration_min = self.min_slider_temps.get()

        genre = self.liste_genres      
        # Changer de fenêtre
        self.master.show_Films(tuple(self.Resultat(annee_max, annee_min, rating_max, rating_min, genre, duration_max, duration_min)))

    def Resultat(self, annee_max, annee_min, rating_max, rating_min, desired_genres, duration_max, duration_min):
        # Recherche des films parmi la base de données

        #variables utiles/ paramètres
        liste_des_films = []
        rating_liste = []
        nombre_de_film = 3


        #si aucun genre est sélectionné
        if len(desired_genres) == 0:
            data = bdd[
                (bdd["startYear"] >= int(annee_min))
                & (bdd["startYear"] <= int(annee_max))
                & (bdd["averageRating"] <= int(rating_max))
                & (bdd["averageRating"] >= int(rating_min))
                & (bdd["averageRating"] >= int(rating_min)) 
                & (bdd["runtimeMinutes"] <= int(duration_max))
                & (bdd["runtimeMinutes"] >= int(duration_min))]
        
        #si la case des genres est cochée
        if self.var.get():
            print(" duration max : ",int(duration_max), int(duration_min))
            data = bdd[
                (bdd["genres"].apply(lambda x: all(genre in x for genre in desired_genres)))
                & (bdd["startYear"] >= int(annee_min))
                & (bdd["startYear"] <= int(annee_max))
                & (bdd["averageRating"] <= int(rating_max))
                & (bdd["averageRating"] >= int(rating_min))
                & (bdd["runtimeMinutes"] <= int(duration_max))
                & (bdd["runtimeMinutes"] >= int(duration_min))
            ]

        #si la case des genres n'est pas cochée
        else:
            data = bdd[
                (bdd["genres"].apply(lambda x: any(genre in x for genre in desired_genres)))
                & (bdd["startYear"] >= int(annee_min))
                & (bdd["startYear"] <= int(annee_max))
                & (bdd["averageRating"] <= int(rating_max))
                & (bdd["averageRating"] >= int(rating_min))
                & (bdd["runtimeMinutes"] <= int(duration_max))
                & (bdd["runtimeMinutes"] >= int(duration_min))
            ]


        # Chargement de la blacklist
        try:
            with open("data/blacklist.json") as file:

                blacklist = json.load(file)
        except FileNotFoundError:
            blacklist = []
        
        

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


        # si la recherche renvoie plus de 9 films, on ajoute des films au hasard, mais biaisé pour que le rating soit plus élevé
        if len(data) > nombre_de_film*3:
            print("nombre de film : ", nombre_de_film)
            for i in range(0, nombre_de_film*3):
                while (True):
                    idFilm = data.sample(1)
                    rating_liste.append([idFilm["averageRating"].values[0], idFilm.index[0]])
                    if idFilm not in blacklist:
                        break
            rating_liste.sort(reverse=True)
            # on ajoute les 3 meilleurs films
            for i in range(0, 3):
                liste_des_films.append(rating_liste[i][1])
                blacklist.append(rating_liste[i][1])
        
        #si la recherche renvoie moins de 9 films, on ajoute des films au hasard
        else:
            print(nombre_de_film)
            for i in range(0, nombre_de_film):
                while (True):
                    idFilm = data.sample(1).index[0]
                    if idFilm not in blacklist:
                        break
                blacklist.append(idFilm)
                liste_des_films.append(idFilm)
        
        return liste_des_films



    
    # visuel de la recherhe
    def create_widgets(self):

        ctk.set_appearance_mode("dark")
        

        ########## DIVERS ###############

        # Titre
        self.Titre = ctk.CTkLabel(self, text="Sélecteur-Film-3000", font=("Arial", 30, "bold"), justify="center", text_color = BUTTON_COLOR)
        self.Titre.place(relx=0.5, rely=0.05, anchor="center")

        # Bouton de recherche
        self.collect_button = ctk.CTkButton(self, text="Collecter", command=self.collect_info, font=("Arial", 14),fg_color=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR, hover_color= BUTTON_COLOR_HOVER ,width=60, height=60, corner_radius=32)
        self.collect_button.place(relx=0.6, rely=0.6, relwidth=0.3)

        ########### SLIDER #############
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

        
        ########## GENRES ##########

        # Définir la liste des genres avant de l'utiliser
        self.liste_des_genres = list(genres.value_to_key.keys())

        # Variable pour stocker la sélection
        n = tk.StringVar()
        n = self.liste_des_genres

        self.add_Genre = ctk.CTkButton(self, text="+", command=self.add_genres, fg_color=BUTTON_COLOR, text_color=BUTTON_TEXT_COLOR, hover_color= BUTTON_COLOR_HOVER ,width=25, height=25, corner_radius=15, font=("Arial", 12))
        self.add_Genre.place(relx=0.40, rely=0.40, anchor="center")

        self.choixGenre = ttk.Combobox(self, width=19, font=("Arial", 12), justify="center", values=n)
        self.choixGenre.place(relx=0.23, rely=0.40, anchor="center")
        self.choixGenre.set("")

        # Associer la fonction de recherche au combobox
        self.choixGenre.bind("<KeyRelease>", self.recherche_Liste)

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
        self.ajout_de_genre.place(relx=0.25, rely=0.65, anchor="center")

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
    
        )
        self.supprimer_genre_button.place(relx=0.40, rely=0.65, anchor="center")
        

        self.var = tk.BooleanVar()  # Peut prendre les valeurs True ou False

        # Ajouter une case à cocher
        self.checkbox_label = tk.Label(self, text="Genre spécifique", font=("Arial", 12), background=BACKGROUND_COLOR, fg=COLOR_WHITE)
        self.checkbox = tk.Checkbutton(self, variable=self.var, onvalue=True, offvalue=False, width=2, height=1, indicatoron=False , fg="black", bg="#4f574f", activebackground=BACKGROUND_COLOR, activeforeground=COLOR_WHITE)
        self.checkbox_label.place(relx=0.68, rely=0.7, relwidth=0.2)
        self.checkbox.place(relx=0.64, rely=0.7, relwidth=0.05 )


    ######### Update Slider ############

    #années SLIDER
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

    #Rating SLIDER
    def update_range_rating(self, value):
        min_val = int(self.min_slider_rating.get())
        max_val = int(self.max_slider_rating.get())
        # Empêcher que min dépasse max
        if min_val >= max_val:
            self.min_slider_rating.set(max_val - 1)
        # Empêcher que max soit infériror à min
        if max_val <= min_val:
            self.max_slider_rating.set(min_val + 1)
        mi = round(int(self.min_slider_rating.get())*0.1,1)
        ma = round(int(self.max_slider_rating.get())*0.1,1)
        
        print(mi,ma)
        self.range_label_rating.configure(text=f"Rating min: {mi} -  Rating max: {ma}")

    #Durations SLIDER
    def update_range_Temps(self, value):
        min_val = int(self.min_slider_temps.get())
        max_val = int(self.max_slider_temps.get())
        # Empêcher que min dépasse max
        if min_val >= max_val:
            self.min_slider_temps.set(max_val - 1)
        # Empêcher que max soit infériror à min
        if max_val <= min_val:
            self.max_slider_temps.set(min_val + 1)
        self.range_label_temps.configure(text=f"Duration min: {int(self.min_slider_temps.get())} -  Duration max: {int(self.max_slider_temps.get())}")

    ############## Genres ################

    # Supprimer un genre
    def supprimer_genre(self, val):
        selection = self.supprimer_genre_button.curselection()
        if selection:
            index = selection[0]
            value = self.ajout_de_genre.get(index)
            self.ajout_de_genre.delete(index)
            decoded_value = BDD.genre_encode(value)

            if decoded_value in self.liste_genres:
                print("decoded value found in liste_genres")
                self.liste_genres.remove(decoded_value)
            else:
                print("decoded value not found in liste_genres")
            
            self.after(100, lambda: self.supprimer_genre_button.delete(index))
            #prévention d'un bug de suppression

    # Ajouter un genre
    def add_genres(self):
        #tester si le genre existe + s'il est deja ajouté
        if self.genres_exist(self.choixGenre.get()) or (BDD.genre_encode(self.choixGenre.get()) in self.liste_genres):
            print("mauvaise entrée")
            self.choixGenre.configure(foreground="red")
        else:
            self.choixGenre.configure(foreground="green")
            self.liste_genres.append(BDD.genre_encode(self.choixGenre.get()))
            self.ajout_de_genre.insert(ctk.END, self.choixGenre.get())
            self.choixGenre.set("")
            self.supprimer_genre_button.insert(ctk.END, "X")
    
    # Fonction de recherche

    def recherche_Liste(self, event):

        value = event.widget.get()
        if value == "":
            self.choixGenre["values"] = self.liste_des_genres
        else:
            # Filtrer les genres en fonction de la saisie
            data = [item for item in self.liste_des_genres if value.lower()
                    in item.lower()]
            self.choixGenre["values"] = data
    
    # assure de ne pas ajouter un genre qui n'existe pas
    def genres_exist(self, entry):
        if entry not in genres:
            return True
        else:
            return False
        

