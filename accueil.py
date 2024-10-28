import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Accueil(ctk.CTkFrame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()


    def create_widgets(self):
        # Grille
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        # Nom
        self.name_label = ctk.CTkLabel(self, text="Nom:")
        self.name_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Entrez votre nom")
        self.name_entry.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")
        # Email
        self.email_label = ctk.CTkLabel(self, text="Email:")
        self.email_label.grid(row=1, column=0, padx=20, pady=(10,10), sticky="w")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Entrez votre email")
        self.email_entry.grid(row=1, column=1, padx=20, pady=(10,10), sticky="ew")
        # Genre
        self.gender_label = ctk.CTkLabel(self, text="Genre:")
        self.gender_label.grid(row=2, column=0, padx=20, pady=(10,10), sticky="w")
        self.gender_var = tk.StringVar(value="Non spécifié")
        self.gender_male_rb = ctk.CTkRadioButton(self, text="Homme", variable=self.gender_var,
        value="Homme")
        self.gender_male_rb.grid(row=2, column=1, padx=20, pady=(10,10), sticky="w")
        self.gender_female_rb = ctk.CTkRadioButton(self, text="Femme", variable=self.gender_var,
        value="Femme")
        self.gender_female_rb.grid(row=3, column=1, padx=20, pady=(10,10), sticky="w")
        # Langues parlées
        self.languages_label = ctk.CTkLabel(self, text="Langues parlées:")
        self.languages_label.grid(row=4, column=0, padx=20, pady=(10,10), sticky="w")
        self.languages = ["Français", "Anglais", "Espagnol"]
        self.language_vars = {lang: tk.BooleanVar() for lang in self.languages}
        i=5
        for index, language in enumerate(self.languages):
            cb = ctk.CTkCheckBox(self, text=language, variable=self.language_vars[language])
            cb.grid(row=i, column=1, padx=20, pady=(10,10), sticky="w")
            i+=1
        # Message
        self.message_label = ctk.CTkLabel(self, text="Message:")
        self.message_label.grid(row=8, column=0, padx=20, pady=(10,10), sticky="nw")
        self.message_text = tk.Text(self, height=5, width=30)
        self.message_text.grid(row=8, column=1, padx=20, pady=(10,10), sticky="ew")
        # Bouton de soumission
        self.submit_button = ctk.CTkButton(self, text="Soumettre", command=self.submit_form)
        self.submit_button.grid(row=9, column=0, columnspan=2, padx=20, pady=20)
    def submit_form(self):
        print("Nom:", self.name_entry.get())
        print("Email:", self.email_entry.get())
        print("Genre:", self.gender_var.get())
        print("Langues:", ', '.join([language for language, var in self.language_vars.items() if var.get()]))
        print("Message:", self.message_text.get("1.0", tk.END))


    def Submit_callBack(self):
        print("button clicked")
        self.label.configure(text="Vous avez cliqué sur le bouton")

