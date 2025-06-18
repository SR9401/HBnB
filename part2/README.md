<<<<<<< HEAD
# Partie 2 : Implémentation de la logique métier et des points de terminaison de l'API

Dans cette partie du projet **HBnB**, vous entrez dans la phase d’implémentation de l’application, basée sur la conception réalisée dans la partie précédente. L’objectif principal est de construire les couches **Présentation** et **Logique Métier** de l’application en utilisant **Python** et **Flask**.

Vous allez définir les classes, les méthodes et les points de terminaison nécessaires pour former le cœur fonctionnel de l’application.

---

## 🎯 Objectifs

### 🧱 Mise en place de la structure du projet
- Organiser le projet selon une architecture modulaire, en suivant les bonnes pratiques des applications Python/Flask.
- Créer les packages nécessaires pour les couches **Présentation** et **Logique Métier**.

### ⚙️ Implémentation de la couche de logique métier
- Développer les classes principales : `User`, `Place`, `Review`, `Amenity`.
- Implémenter les relations entre entités et leur interaction dans l’application.
- Appliquer le **pattern facade** pour simplifier la communication entre la Présentation et la Logique Métier.

### 🌐 Construction de l’API REST
- Créer les endpoints pour les opérations CRUD sur les entités principales.
- Utiliser **flask-restx** pour définir et documenter l’API de manière cohérente.
- Implémenter la sérialisation des données pour inclure les attributs liés (ex : lors de la récupération d’un lieu, inclure le prénom, nom du propriétaire et les commodités associées).

### 🧪 Test et validation
- Vérifier le bon fonctionnement de chaque endpoint et gérer les cas limites.
- Utiliser des outils comme **Postman** ou **cURL** pour tester les routes API.

---

## 🖼️ Vision et portée du projet

Cette partie vise à créer une base **fonctionnelle** et **scalable** pour l’application :

- **Couche Présentation** : Définir les services et routes API en utilisant Flask et flask-restx, avec une structure claire.
- **Couche Logique Métier** : Modéliser la logique principale de l'application (validations, relations, interactions entre objets).

**NB** : L’authentification JWT et le contrôle d’accès par rôle seront abordés dans la Partie 3. Il est donc important de garder une architecture modulaire pour faciliter leur intégration ultérieure.
=======
# ⭐ Exigé par l’énoncé GitHub – Section "Document the Project Setup"

## HBnB Project – Part 2

This project is structured to follow a modular Python architecture with Flask and Flask-RESTx.

### Structure Overview
- `app/` contains all application logic (API, models, services, persistence)
- `run.py` launches the Flask app
- `config.py` manages environment configurations
- `requirements.txt` lists required Python packages
>>>>>>> 4b9aab4 (class usser debut)
