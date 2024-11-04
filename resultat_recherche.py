import customtkinter as ctk
import tkinter as tk
from TMDPAPI import TMDB
from PIL import ImageTk, Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import popularity
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

requete = TMDB()
idfilm1 = "tt0120915"
idfilm2 = "tt0121765"
idfilm3 = "tt0121766"


class ResultatRecherche(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20,
                  sticky="nsew")  # Main grid layout

        # Main Header Label
        self.label = ctk.CTkLabel(
            self, text="CTkLabel", fg_color="transparent")
        self.label.grid(row=0, column=0, columnspan=4, padx=20, pady=(10, 10))

        # Add Image
        self.add_image(requete.get_image(idfilm1),
                       row=0, column=1, columnspan=1)
        self.add_image(requete.get_image(idfilm2),
                       row=0, column=2, columnspan=1)
        self.add_image(requete.get_image(idfilm3),
                       row=0, column=3, columnspan=1)

        # Add Graphique
        self.add_graphique(columnspan=3)

        # Information Sections
        self.add_section(
            "Titre:", ["guerres des étoiles", "interstellar", "j'ai compris!!!"], 1)
        self.add_section("Titre original:", ["Star Wars", "b", "c"], 2)
        self.add_section("Année de début:", ["-1000 avjc", "b", "c"], 3)
        self.add_section("Année de fin:", ["-999 avjc", "b", "c"], 4)
        self.add_section("Durée:", ["666", "b", "c"], 5)
        self.add_section("Rating:", ["9/10", "b", "c"], 6)
        self.add_section(
            "Genre(s):", ["action, comedie, romance", "a,d,e", "b,f,g"], 7)

        # Add Description
        self.add_description(requete.get_desc(idfilm1), 1)
        self.add_description(requete.get_desc(idfilm2), 2)
        self.add_description(requete.get_desc(idfilm3), 3)

    def add_description(self, label_text, column):
        label = ctk.CTkLabel(self, text=label_text, wraplength=200)
        label.grid(row=9, column=column, padx=20, pady=(10, 10), sticky="ew")

    def add_section(self, label_text, values, row):
        """Helper function to add a row section to the grid."""
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, padx=20, pady=(10, 10), sticky="ew")
        for i, value in enumerate(values, start=1):
            value_label = ctk.CTkLabel(self, text=value, wraplength=150)
            value_label.grid(row=row, column=i, padx=20,
                             pady=(10, 10), sticky="ew")

    def add_image(self, image_url, row, column, columnspan=1):
        """Helper function to add an image from a URL to the grid."""
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image = image.resize((200, 150))  # Adjust the size as needed
        self.photo = ImageTk.PhotoImage(image)

        # Use text="" to hide text
        image_label = ctk.CTkLabel(self, image=self.photo, text="")
        image_label.grid(row=row, column=column,
                         columnspan=columnspan, padx=20, pady=20, sticky="ew")

    def add_graphique(self, columnspan):
        data = popularity.get_popularity(idfilm1, idfilm2, idfilm3)

        for name, series in data.items():
            plt.plot(data.index, series, label=name)
        plt.legend(loc="upper left")
        # Intégrer le graphique dans tkinter
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(
            row=10, column=1, pady=(10, 10), columnspan=columnspan)
