import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import json
import os
import bdd

'''
    BUT 
    - Ajouter une fonctionnalité de création de profil. 
    - Pouvoir ajouter des films aimés au profil. 
    Réussi !
    
    OBJECTIF SUPP.
    - Que les films aimés soient plus souvent suggérés 
    Non réussi, car j'ai réalisé que c'était une toute autre partie du programme avec 
    laquelle je n'étais pas familier.
    
    DIFFICULTÉ
    - json                              (découverte)
    - profil actif                      (complexe et aller jouer dans d'autres class)
    - passer d'une fenêtre à une autre  (erreurs)

    APPRENTISSAGE
    - json et profil actif !
    - messagebox                        (découverte)
    - tk.Toplevel                       (découverte)

    MODIFICATION POSSIBLE
    - ne pas avoir deux fois le même film liké dans la liste de film liké
''' 


class Profil(tk.Frame):

    def __init__(self,profil_actif, master=None,fichier_profil="profils.json"):
        super().__init__(master)
        self.master = master
        self.fichier_profil = fichier_profil
        self.liste_profil = self.charger_profils()
        self.profil_actif = profil_actif
        self.create_widgets()

        #Style
        ctk.set_appearance_mode("dark")

        style = ttk.Style()
        style.theme_use("clam")  
        style.configure("TButton", font=("Helvetica", 12), padding=6)


    def create_widgets(self):
        
        #Grid principal
        self.grid(row=0, column=0, padx=80, pady=20, sticky="nsew")
        
        #Choisir un profil
        n = tk.StringVar()

        # Combobox pour choisir un profil
        self.label_choixprofil = ctk.CTkLabel(self, text="Choisir un profil:", text_color="black")
        self.label_choixprofil.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.choixprofil = ttk.Combobox(self, width=20, textvariable=n)
        self.choixprofil.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.update_combobox()
        self.choixprofil.set("")  # Valeur par défaut vide

        # Événement pour changer le profil actif
        self.choixprofil.bind("<<ComboboxSelected>>", self.update_profil_actif)
        
        #LABEL
        # Label pour nom
        self.label_nom = ctk.CTkLabel(self, text="Nom:", text_color="black")
        self.label_nom.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.entry_nom = ctk.CTkEntry(self, placeholder_text="unknown")
        self.entry_nom.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Label pour email
        self.label_email = ctk.CTkLabel(self, text="Email:", text_color="black")
        self.label_email.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.entry_email = ctk.CTkEntry(self, placeholder_text="unknown")
        self.entry_email.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Label pour age
        self.label_age = ctk.CTkLabel(self, text="Age:", text_color="black")
        self.label_age.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.entry_age = ctk.CTkEntry(self, placeholder_text="unknown")
        self.entry_age.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        #BOUTON
        # Bouton pour créer un profil
        self.créerleprofil = ctk.CTkButton(self, text="Créer le profil",  command=self.créer_le_profil
                                             ,fg_color="#424242", hover_color="#636363",text_color="white")
        self.créerleprofil.grid(row=5, column=1, padx=10, pady=20, sticky="w")
        
        # Bouton pour continuer
        self.continuu = ctk.CTkButton(self, text="Continuer", command=self.goto_accueil
                                    ,fg_color="#424242", hover_color="#636363",text_color="white")
        self.continuu.grid(row=6, column=1, padx=10, pady=20, sticky="w")
        
        # Bouton pour supprimer un profil
        self.destroyy = ctk.CTkButton(self, text="Supprimer le profil",  command=self.destroyprofil
                                      ,fg_color="#424242", hover_color="#636363",text_color="white")
        self.destroyy.grid(row=7, column=1, padx=10, pady=20, sticky="w")

        # Bouton pour afficher les informations associées à un profil
        self.affiche_info = ctk.CTkButton(self, text="Afficher les informations du profil", command=self.afficher_info_profil
                                          ,fg_color="#424242", hover_color="#636363",text_color="white")
        self.affiche_info.grid(row=8, column=1, padx=10, pady=20, sticky="w")
        
        # Bouton pour voir les films liké
        self.likeeee = ctk.CTkButton(self, text="Voir les films liké", command=self.afficherfilmliké
                                     ,fg_color="#424242", hover_color="#636363",text_color="white")
        self.likeeee.grid(row=9, column=1, padx=10, pady=20, sticky="w")
        
        # Bouton pour supprimer un film liké
        self.suppp = ctk.CTkButton(self, text="Supprimer le dernier film liké", command=self.suppfilmliké
                                    ,fg_color="#424242", hover_color="#636363",text_color="white")
        self.suppp.grid(row=10, column=1, padx=10, pady=20, sticky="w")


    def suppfilmliké(self): #supprime le dernier film liké
        if not self.profil_actif:
            tk.messagebox.showerror("Erreur", "Aucun profil actif sélectionné")
            return
        
        for profil in self.liste_profil:
            if profil["nom"] == self.profil_actif:
                films_likes = profil.get("films_likés", [])
                if not films_likes:
                    tk.messagebox.showinfo("Info", "Aucun film à supprimer")
                    return
                
                dernier_film = films_likes[-1]

                confirmation = tk.messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer le dernier film liké '{bdd.get_title(dernier_film)}' ?")
                if not confirmation:
                    return

                films_likes.pop()
                self.sauvegarder_profils()
                tk.messagebox.showinfo("Info", f"Le dernier film liké, '{bdd.get_title(dernier_film)}', a été supprimé")
                return


    def afficherfilmliké(self): #Affiche les films likés du profil actif.
        if not self.profil_actif:
            tk.messagebox.showerror("Erreur", "Aucun profil actif sélectionné.")
            return

        # Récupérer le profil actif
        for profil in self.liste_profil:
            if profil["nom"] == self.profil_actif:
                films_likes = profil.get("films_likés", [])
                break
        else:
            tk.messagebox.showerror("Erreur", "Profil non trouvé.")
            return

        # Créer une nouvelle fenêtre pour afficher les films
        fenetre_films = tk.Toplevel(self) #indépendante, mais liée à la fenêtre principale
        fenetre_films.title(f"Films likés de {self.profil_actif}")
        fenetre_films.geometry("400x300")

        if not films_likes:
            label = tk.Label(fenetre_films, text="Aucun film liké.", font=("Arial", 12))
            label.pack(pady=20)
        else: 
            # Ajouter une liste de films
            for film in films_likes:
                label = tk.Label(fenetre_films, text=f"- {bdd.get_title(film)}", font=("Arial", 10))
                label.pack(anchor="w", padx=10, pady=2)


    def goto_accueil(self):    
        if not self.profil_actif:
            tk.messagebox.showerror("Erreur", "Veuillez sélectionner un profil pour continuer.")
            return
        else:
            self.master.show_accueil(self.profil_actif)
        

    def update_profil_actif(self, event): # Met à jour profil_actif avec le profil sélectionné
        selected_profile = self.choixprofil.get()  # Récupère la valeur de la combobox
        self.profil_actif = selected_profile  # Met à jour profil_actif
        #print(f"Profil actif sélectionné: {self.profil_actif}")

    
    def update_combobox(self): # Met à jour les valeurs de la combobox
        self.choixprofil["values"] = [profil["nom"] for profil in self.liste_profil]


    def destroyprofil(self): # Supprimer un profil
        # Vérification préliminaire
        if not self.profil_actif:
            tk.messagebox.showerror("Erreur", "Aucun profil actif sélectionné pour suppression.")
            return
        
        # Confirmer la suppression
        confirmation = tk.messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer le profil '{self.profil_actif}' ?")
        if not confirmation:
            return
        
        # Supprimer le profil actif de la liste
        self.liste_profil = [profil for profil in self.liste_profil if profil["nom"] != self.profil_actif] 
        
        # Sauvegarder la liste mise à jour
        self.sauvegarder_profils() 
        
        # Mettre à jour la combobox
        self.update_combobox()  
        
        # Réinitialiser le profil actif
        self.profil_actif = ""  
        self.choixprofil.set("")  # Efface la sélection dans la combobox
        
        # Afficher le succès de l'opération
        tk.messagebox.showinfo("Succès", "Le profil a été supprimé avec succès.")
    

    def afficher_info_profil(self):
        if not self.profil_actif:
            tk.messagebox.showerror("Erreur", "Aucun profil actif sélectionné pour afficher les informations.")
            return
        else:
            for profil in self.liste_profil:
                if profil["nom"] == self.profil_actif:
                    email = profil.get("email")
                    age = profil.get("age")
            
            tk.messagebox.showinfo("Informations ", f" - Nom : {self.profil_actif} \n - Email : {email} \n - Age : {age}")

    
    def créer_le_profil(self):
        if self.entry_nom.get() == "":
            tk.messagebox.showerror("Erreur", "Aucun nom donné au profil.")
        else:
            # Créer une personne à partir des informations fournies
            personne = {"nom" : self.entry_nom.get(), "email" : self.entry_email.get(),"age" : self.entry_age.get(),"films_likés": [] }
            
            # Ajoute la personnee à la liste de profil
            self.liste_profil.append(personne)
            
            # Sauvegarde la liste mise à jour
            self.sauvegarder_profils()
            
            # Met à jour la combobox
            self.update_combobox()

            # Vider les champs après ajout
            self.entry_nom.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_age.delete(0, tk.END)


    def ajouter_film_au_profil(self, nom_profil, film):
        """Ajoute un film liké au profil spécifié."""
        for profil in self.liste_profil:
            if profil["nom"] == nom_profil:
                profil["films_likés"].append(film)
                self.sauvegarder_profils()
                break


    def sauvegarder_profils(self):
        """Sauvegarde la liste des profils dans un fichier JSON."""
        with open(self.fichier_profil, "w") as fichier:
            json.dump(self.liste_profil, fichier, indent=4)


    def charger_profils(self):
        """Charge la liste des profils depuis un fichier JSON."""
        if os.path.exists(self.fichier_profil):
            with open(self.fichier_profil, "r") as fichier:
                profils = json.load(fichier)
                for profil in profils:
                    if 'films_likés' not in profil:
                        profil['films_likés'] = []  # Initialise avec une liste vide si absent
                return profils
        return []
    
    

    

