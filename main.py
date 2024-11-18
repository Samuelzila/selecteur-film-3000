import customtkinter as ctk
from accueil import Accueil
from resultat_recherche import ResultatRecherche


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sélecteur-Film-3000")
        self.geometry("720x640")
        self._set_appearance_mode("dark")
        self.show_accueil()

    def show_accueil(self):
        """
        La page d'accueil, où les filtres sont.
        """
        self.clear_main_frame()
        self.accueil = Accueil(master=self)
        self.accueil.pack(fill="both", expand=True)

    def show_Films(self, idfilms):
        """
        L'affichage des trois films résultants.
        """
        self.clear_main_frame()
        self.resultat_recherche = ResultatRecherche(idfilms,
                                                    master=self, width=1280, height=720, corner_radius=0, fg_color="transparent")
        self.resultat_recherche.pack(fill="both", expand=True)

    def clear_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()




if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
    
