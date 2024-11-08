import customtkinter as ctk
from accueil import Accueil
import tkinter as tk  # Importer tkinter pour les menus traditionnels
from resultat_recherche import ResultatRecherche
import numpy as np


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sélecteur-Film-3000")
        self.show_Films()

    def show_accueil(self):
        self.clear_main_frame()
        self.accueil = Accueil(master=self)
        self.accueil.pack(fill="both", expand=True)

    def show_Films(self):
        self.clear_main_frame()
        self.resultat_recherche = ResultatRecherche(self)
        self.resultat_recherche.pack(fill="both", expand=True)

    def clear_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
