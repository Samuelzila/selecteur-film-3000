import customtkinter as ctk
from TMDPAPI import TMDB
from PIL import ImageTk, Image
import requests
from io import BytesIO
import bdd
import matplotlib.pyplot as plt
import popularity
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
import json

requete = TMDB()


class ResultatRecherche(ctk.CTkScrollableFrame):
    def __init__(self, idfilms, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.idfilms = idfilms
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20,
                  sticky="nsew")  # Main grid layout

        # Force la colonne centrale à prendre de l'espace pour centrer les éléments.
        # Utile si le graphique ne s'affiche pas.
        self.grid_columnconfigure(2, weight=1)

        # Main Header Label
        self.label = ctk.CTkLabel(
            self, text="CTkLabel", fg_color="transparent")
        self.label.grid(row=0, column=0, columnspan=4, padx=20, pady=(10, 10))

        # Add Image
        self.add_image(requete.get_image(self.idfilms[0]),
                       row=0, column=1, columnspan=1)
        self.add_image(requete.get_image(self.idfilms[1]),
                       row=0, column=2, columnspan=1)
        self.add_image(requete.get_image(self.idfilms[2]),
                       row=0, column=3, columnspan=1)

        # Add Graphique
        self.add_graphique(columnspan=3)

        # Information Sections
        self.add_section("Titre:", [bdd.get_title(
            self.idfilms[0]), bdd.get_title(self.idfilms[1]), bdd.get_title(self.idfilms[2])], 1)
        self.add_section("Titre original:", [bdd.get_originaltitle(
            self.idfilms[0]), bdd.get_originaltitle(self.idfilms[1]), bdd.get_originaltitle(self.idfilms[2])], 2)
        self.add_section("Année de début:", [bdd.get_startYear(
            self.idfilms[0]), bdd.get_startYear(self.idfilms[1]), bdd.get_startYear(self.idfilms[2])], 3)
        self.add_section("Rating (sur 10):", [bdd.get_rating(
            self.idfilms[0]), bdd.get_rating(self.idfilms[1]), bdd.get_rating(self.idfilms[2])], 4)
        # self.add_section("Année de fin:", [bdd.get_endYear(idfilm1), bdd.get_endYear(idfilm2), bdd.get_endYear(idfilm3)], 4)
        self.add_section("Durée (minutes):", [bdd.get_runtime(
            self.idfilms[0]), bdd.get_runtime(self.idfilms[1]), bdd.get_runtime(self.idfilms[2])], 5)
        self.add_section("Genre(s):", [", ".join(bdd.get_genres(
            self.idfilms[0])), ", ".join(bdd.get_genres(self.idfilms[1])), ", ".join(bdd.get_genres(self.idfilms[2]))], 7)

        # Add Description
        self.add_description(requete.get_desc(self.idfilms[0]), 1)
        self.add_description(requete.get_desc(self.idfilms[1]), 2)
        self.add_description(requete.get_desc(self.idfilms[2]), 3)

        button = ctk.CTkButton(
            self, text="Ne plus afficher", command=partial(self.ne_plus_afficher, self.idfilms[0]))
        button.grid(row=10, column=1)
        button = ctk.CTkButton(
            self, text="Ne plus afficher", command=partial(self.ne_plus_afficher, self.idfilms[1]))
        button.grid(row=10, column=2)
        button = ctk.CTkButton(
            self, text="Ne plus afficher", command=partial(self.ne_plus_afficher, self.idfilms[2]))
        button.grid(row=10, column=3)

    def ne_plus_afficher(self, id):
        """
        Ajouter un film dans la blacklist.
        """
        try:
            file = open("./data/blacklist.json")
            blacklist = json.load(file)
            file.close()
        except FileNotFoundError:
            blacklist = []

        blacklist.append(id)

        with open("./data/blacklist.json", "w") as file:
            json.dump(blacklist, file)

    def add_description(self, label_text, column):
        """Helper function to add a description to the grid."""
        if requete:
            label = ctk.CTkLabel(self, text=label_text, wraplength=200)
            label.grid(row=9, column=column, padx=20,
                       pady=(10, 10), sticky="ew")
        else:
            label = ctk.CTkLabel(self, text="", wraplength=200)
            label.grid(row=9, column=column, padx=20,
                       pady=(10, 10), sticky="ew")

    def add_section(self, label_text, values, row):
        """Helper function to add a row section to the grid."""
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, padx=20, pady=(10, 10), sticky="ew")
        for i, value in enumerate(values, start=1):
            value_label = ctk.CTkLabel(self, text=str(value), wraplength=150)
            value_label.grid(row=row, column=i, padx=20,
                             pady=(10, 10), sticky="ew")

    def add_image(self, image_url, row, column, columnspan=1):
        """Helper function to add an image to the grid."""
        if requete:
            if image_url is not None:
                try:
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    # Adjust the size as needed
                    image = image.resize((120, 150))
                    self.photo = ImageTk.PhotoImage(image)
                    # Use text="" to hide text
                    image_label = ctk.CTkLabel(self, image=self.photo, text="")
                    image_label.grid(
                        row=row, column=column, columnspan=columnspan, padx=20, pady=20, sticky="ew")
                except Exception:
                    self.add_no_image_available(row, column, columnspan)
            else:
                self.add_no_image_available(row, column, columnspan)
        else:
            self.add_no_image_available(row, column, columnspan)

    def add_graphique(self, columnspan):
        """Helper function to add a chart to the grid."""
        data = popularity.get_popularity(
            self.idfilms[0], self.idfilms[1], self.idfilms[2])

        if data is not None:
            plt.figure(figsize=(10, 3))

            for name, series in data.items():
                plt.plot(data.index, series, label=name)
            plt.legend(loc="upper left")
            # Intégrer le graphique dans tkinter
            self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(
                row=11, column=1, pady=(10, 10), columnspan=columnspan)

    def add_no_image_available(self, row, column, columnspan):
        """
        Image par défaut si aucune image n'a pue être trouvée.
        """
        image = Image.open("no_image_available.jpg")
        image = image.resize((120, 150))  # Adjust the size as needed
        self.photo = ImageTk.PhotoImage(image)
        # Use text="" to hide text
        image_label = ctk.CTkLabel(self, image=self.photo, text="")
        image_label.grid(row=row, column=column,
                         columnspan=columnspan, padx=20, pady=20, sticky="ew")
