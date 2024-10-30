import customtkinter as ctk
import tkinter as tk
from PIL import ImageTk, Image 
class ResultatRecherche(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")  # Main grid layout

        # Main Header Label
        self.label = ctk.CTkLabel(self, text="CTkLabel", fg_color="transparent")
        self.label.grid(row=0, column=0, columnspan=4, padx=20, pady=(10, 10))

        # Film Labels
        film_titles = ["Film 1", "Film 2", "Film 3"]
        for i, title in enumerate(film_titles, start=1):
            film_label = ctk.CTkLabel(self, text=title)
            film_label.grid(row=0, column=i, padx=20, pady=(10, 10), sticky="ew")

        # Information Sections
        self.add_section("Titre:", ["guerres des étoiles", "interstellar", "j'ai compris!!!"], 1)
        self.add_section("Titre original:", ["Star Wars", "b", "c"], 2)
        self.add_section("Année de début:", ["-1000 avjc", "b", "c"], 3)
        self.add_section("Année de fin:", ["-999 avjc", "b", "c"], 4)
        self.add_section("Durée:", ["666", "b", "c"], 5)
        self.add_section("Rating:", ["9/10", "b", "c"], 6)
        self.add_section("Genre(s):", ["action, comedie, romance", "a,d,e", "b,f,g"], 7)

        # Add Image
        self.add_image(r"C:\Users\Eric Benoit\OneDrive\Desktop\BUREAU\Cegep\starwars.png", row=8, column=0, columnspan=3)

        #Add Description
        

    def add_section(self, label_text, values, row):
        """Helper function to add a row section to the grid."""
        label = ctk.CTkLabel(self, text=label_text)
        label.grid(row=row, column=0, padx=20, pady=(10, 10), sticky="w")
        for i, value in enumerate(values, start=1):
            value_label = ctk.CTkLabel(self, text=value)
            value_label.grid(row=row, column=i, padx=20, pady=(10, 10), sticky="ew")

    def add_image(self, image_path, row, column, columnspan=1):
        """Helper function to add an image to the grid."""
        image = Image.open(image_path)
        image = image.resize((150, 100))  # Adjust the size as needed
        self.photo = ImageTk.PhotoImage(image)

        image_label = ctk.CTkLabel(self, image=self.photo, text="")  # Use text="" to hide text
        image_label.grid(row=row, column=column, columnspan=columnspan, padx=20, pady=20, sticky="ew")
    
       

      
    
    