# Utiliser l'image officielle Selenium avec Firefox
FROM selenium/standalone-firefox:latest

# Installer Python
RUN sudo apt-get update && sudo apt-get install -y python3 python3-pip

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY app /app/app

# Installer les dépendances Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Exposer le port si nécessaire
EXPOSE 80

# Commande pour exécuter l'application
CMD ["python3", "app/main.py"]