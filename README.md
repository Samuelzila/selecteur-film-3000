# selecteur-film-3000
Un outil qui choisit des films pour les indécis.

# Utilisation
Installez les dépendances.
`pip install -r requirements.txt`
Il se peut que vous ayez besoin d'installer tkinter manuellement.

Renommez .env.example en .env et remplaces les xxx par une clef vers l'API de TMDB. Le code devrait quand même fonctionner sans, mais de manière limitée.

# Mettre à jour les bases de données.
Les bases de données sont disponibles aux liens suivants:
- https://datasets.imdbws.com/title.basics.tsv.gz
- https://datasets.imdbws.com/title.ratings.tsv.gz
Elles doivent être placées dans data/

Le code est conçu pour supporter les fichiers tels quels, mais vous pouvez exécuter data/db_cleaner.py afin de réduire considérablement leur taille et accélérer le programme.
