import os
import requests
from dotenv import load_dotenv


class TMDB:
    """
    Classe pour faire des requêtes vers l'api de TMDB
    """

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")

    def get_desc(self, imdb_id):
        """
        Obtenir la description d'un film à partir de son identifiant unique iMDB
        """
        try:
            resp = requests.get(
                f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={self.api_key}&external_source=imdb_id")
            return resp.json()["movie_results"][0]["overview"]
        except Exception:
            return ""

    def get_image(self, imdb_id):
        """
        Obtenir le lien de l'image d'un film à partir de son id iMDB
        """
        try:
            resp = requests.get(
                f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={self.api_key}&external_source=imdb_id")
            poster_path = resp.json()["movie_results"][0]["poster_path"]
            return f"https://image.tmdb.org/t/p/original/{poster_path}"
        except:
            return None

    def __bool__(self):
        """
        Retourne si le programme a pu lire le .env
        """
        try:
            resp = requests.get(
                f"https://api.themoviedb.org/3/authentication?api_key={self.api_key}")
            return resp.ok
        except Exception:
            return False
