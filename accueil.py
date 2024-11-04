import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

class Accueil(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.liste_3_genres = []
        

    def collect_info(self):
            
            if not self.entry_annee_max.get().isdigit() or not self.entry_annee_min.get().isdigit() or not self.entry_rating_max.get().isdigit() or not self.entry_rating_min.get().isdigit():
                self.show_invalid_entry()
            else:
                # Collecte des informations entrées par l'utilisateur
                annee_max = self.entry_rating_min.get()
                annee_min = self.entry_annee_min.get()
                rating_max = self.entry_rating_max.get()
                rating_min = self.entry_rating_min.get()
                genre = self.choixGenre.get()

                # Afficher les informations dans la console pour vérification
                print("Année Max :", annee_max)
                print("Année Min :", annee_min)
                print("Rating Max :", rating_max)
                print("Rating Min :", rating_min)
                print("Genre sélectionné :", genre)
    
    def show_invalid_entry(self):
        ctk.CTkLabel(self, text="Veuillez entrer des valeurs valides.", text_color="red").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        
        if self.entry_annee_max.get().isdigit():
            self.entry_annee_max._bg_color = "white"
        else:
            self

        if self.entry_annee_min.get().isdigit():
            self.entry_annee_min._text_color = "red"
        else:
            self.entry_annee_min._bg_color = "white"

        if self.entry_rating_max.get().isdigit():
            self.entry_rating_max._bg_color = "red"
        else:
            self.entry_rating_max._bg_color = "white"

        if self.entry_rating_min.get().isdigit():
            self.entry_rating_min._fg_color = "red"
        else:
            self.entry_rating_min._bg_color = "white"
    
    def add_genres(self):
        self.liste_3_genres.append(self.choixGenre.get())

    def create_widgets(self):
        self.grid(row=0, column=0, padx=80, pady=20, sticky="nsew")
        
        # Définir la liste des genres avant de l'utiliser
        liste_des_genres = ('January', 'February', 'March', 'April', 'May', 
                            'June', 'July', 'August', 'September', 'October', 
                            'November', 'December')

        # Variable pour stocker la sélection
        n = tk.StringVar()

        # Création de labels et entrées pour les années
        self.label_annee_max = ctk.CTkLabel(self, text="Année Max:", text_color="black")
        self.label_annee_max.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_annee_max = ctk.CTkEntry(self, placeholder_text="2000")
        self.entry_annee_max.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_annee_min = ctk.CTkLabel(self, text="Année Min:", text_color="black")
        self.label_annee_min.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.entry_annee_min = ctk.CTkEntry(self, placeholder_text="2000")
        self.entry_annee_min.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Création de labels et entrées pour les Rating
        self.label_rating_max = ctk.CTkLabel(self, text="Rating Max:", text_color="black")
        self.label_rating_max.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        self.entry_rating_max = ctk.CTkEntry(self, placeholder_text="2000")
        self.entry_rating_max.grid(row=1, column=4, padx=10, pady=5, sticky="w")

        self.label_rating_min = ctk.CTkLabel(self, text="Rating Min:", text_color="black")
        self.label_rating_min.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        self.entry_rating_min = ctk.CTkEntry(self, placeholder_text="2000")
        self.entry_rating_min.grid(row=2, column=4, padx=10, pady=5, sticky="w")

        # Bouton pour collecter les informations
        self.collect_button = ctk.CTkButton(self, text="Collecter",  command=self.collect_info)
        self.collect_button.grid(row=3, column=3, padx=10, pady=20, sticky="w")

        self.add_Genre = ctk.CTkButton(self, text="ajouter Genre",  command=self.add_genres, fg_color="gray", text_color="white", hover_color="black")
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
                data = [item for item in liste_des_genres if value.lower() in item.lower()]
                self.choixGenre["values"] = data

        # Associer la fonction de recherche au combobox
        self.choixGenre.bind("<KeyRelease>", recherche_Liste)

        # Configuration des colonnes pour s'assurer que chaque colonne a une taille uniforme
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")


