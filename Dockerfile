# Utiliser l'image officielle Selenium avec Firefox
FROM selenium/standalone-firefox:latest

# Installer Python et venv
USER root
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY app /app/app

# Créer et activer un environnement virtuel
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Installer les dépendances Python dans l'environnement virtuel
RUN pip3 install --no-cache-dir -r requirements.txt

# Changer l'utilisateur pour des raisons de sécurité
USER seluser

# Exposer le port si nécessaire
EXPOSE 80

# Commande pour exécuter l'application
CMD ["python3", "app/main.py"]