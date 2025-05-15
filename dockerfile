# Dockerfile

# Image de base
FROM python:3.11-alpine

# Créer le dossier de travail
WORKDIR /app

# Copier les fichiers du projet
COPY ./src .

# Installer les dépendances si besoin
RUN pip install --no-cache-dir requests pandas

# Commande par défaut (modifiable dans docker-compose)
CMD ["python", "main.py"]