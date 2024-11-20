import customtkinter as ctk
import os
from functools import partial


class Profiles(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.create_widgets()

    def create_widgets(self):
        liste_noms = self.get_users()

        # Un frame qui contient les icônes des utilisateurs
        button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        button_frame.place(rely=0.4, relx=0.5, anchor="center")

        # Pour chaque utilisateur détecté, on crée une icône de connection
        for nom in liste_noms:
            # Crée un string d'initiales à partir d'un nom.
            initiales = "".join([s[0] for s in nom.split(" ")])

            # Groupe pour l'icône et le nom complet
            label_group = ctk.CTkFrame(button_frame, fg_color="transparent")
            # Ajout d'un bouton carré, pour le profil
            icon = ctk.CTkButton(
                label_group, text=initiales, command=partial(self.select_user, nom), width=75, height=75, font=("Arial", 32, "bold"))
            icon.pack()
            label = ctk.CTkLabel(label_group, text=nom)
            label.pack()
            label_group.pack(padx=20, side="left")

        # Bouton pour créer un utilisateur
        create_user = ctk.CTkButton(
            self.master, text="Créer un profil", command=self.master.show_create_user)
        create_user.place(relx=0.5, rely=0.5, anchor="center")

    def select_user(self, user):
        self.master.user = user
        self.master.show_accueil()

    def get_users(self):
        """
        Retourne une liste de string correspondant aux noms des utilisateurs.
        """
        try:
            return [file.replace(".json", "") for file in os.listdir("./users/") if os.path.isfile(os.path.join("./users/", file))]
        except FileNotFoundError:
            return []
