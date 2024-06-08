# Utilise l'image Python officielle en tant qu'image de base
FROM python:3.9

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers du répertoire source local dans le répertoire de travail du conteneur
COPY . /app

# Installe les dépendances Python définies dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port 8765 pour que les clients puissent se connecter à l'application
EXPOSE 8765

# Commande par défaut à exécuter lorsque le conteneur démarre
CMD ["python", "app.py"]
