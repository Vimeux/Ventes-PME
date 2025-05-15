# Projet Ventes PME

Ce projet est une application Python qui utilise Docker pour son déploiement. Il utilise SQLite comme base de données.

## Prérequis

- Docker
- Docker Compose

## Lancement du projet

Pour lancer le projet, exécutez la commande suivante à la racine du projet :

```bash
docker compose up
```

Pour lancer le projet en arrière-plan, utilisez :

```bash
docker compose up -d
```

## Structure du projet

```
.
├── src/               # Code source de l'application
├── dockerfile        # Configuration de l'image Docker
├── compose.yml       # Configuration Docker Compose
└── README.md         # Ce fichier
```

## Base de données

Le projet utilise SQLite comme base de données. Les données sont persistées dans un volume Docker nommé `sqlite_data`.
