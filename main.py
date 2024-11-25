import customtkinter as ctk
from accueil import Accueil
from resultat_recherche import ResultatRecherche
from profil import Profil


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sélecteur-Film-3000")
        self.geometry("1280x720")
        self.profil_actif = None  # Attribut pour stocker le profil actif
        self.show_profil()

    def show_profil(self):
        """
        La page de profil, où on peut créer un profil.
        """
        self.clear_main_frame()
        self.profil = Profil(master=self, profil_actif=self.profil_actif)
        self.profil.pack(fill="both", expand=True)

    def show_accueil(self,profil_actif):
        """
        La page d'accueil, où les filtres sont.
        """
        self.profil_actif = profil_actif  # Stocker le profil actif
        self.clear_main_frame()
        self.accueil = Accueil(master=self)
        self.accueil.pack(fill="both", expand=True)

    def show_Films(self, idfilms):
        """
        L'affichage des trois films résultants.
        """
        self.clear_main_frame()
        self.resultat_recherche = ResultatRecherche(master=self, idfilms=idfilms, profil_actif=self.profil_actif, profil_instance=self.profil, width=1280, height=720, corner_radius=0)
        self.resultat_recherche.pack(fill="both", expand=True)

    def clear_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
