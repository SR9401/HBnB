# 🧩 HBnB – Backend Contribution : Persistence, Auth & ORM Mapping

Ce document couvre notre travail spécifique dans le projet HBnB, centré sur l'intégration de la base de données, la mise en place de l'authentification, et la structuration des entités métiers avec SQLAlchemy.

---

## 🔁 Transition from In-Memory to SQL Database

Nous avons refactoré la logique existante pour passer du stockage en mémoire à une **persistance en base de données** relationnelle à l'aide de **SQLAlchemy**.

- ✅ Ajout d'une configuration persistante via une *application factory*
- ✅ Gestion des sessions via `db.session` dans les repositories
- ✅ Implémentation de `SQLAlchemyRepository` générique avec héritages spécialisés

---

## 🧱 ORM Models & Entity Mapping

Les entités principales de l’application ont été mappées sur des modèles SQLAlchemy complets avec validations et contrôles métier.

### 🔹 Modèles gérés

- `User` – avec hash du mot de passe, rôle `is_admin`, validation d'email
- `Place` – localisation, prix, description, validations géographiques
- `Review` – contenu, notation (si applicable), rattachement à un utilisateur et un logement
- `Amenity` – équipements liés aux logements

### 🔹 Ce que nous avons fait :

- Création des classes avec héritage depuis une base `BaseClass`
- Génération d'UUID pour les identifiants
- Utilisation de `@validates` pour les règles de validation fortes
- Mise en place des méthodes `to_dict()` pour exposer les données

---

## 🛡️ Authentification & Droits

Mise en place d’un **système JWT d’authentification** pour sécuriser les routes selon le rôle utilisateur.

- 🔑 Auth via `flask-jwt-extended`
- 🔐 Création de tokens à la connexion
- 🛂 Sécurisation des endpoints selon :
  - Utilisateur connecté
  - Utilisateur administrateur (`is_admin`)

---

## ⚙️ Accès & Permissions

### ✅ Endpoints utilisateurs :

- Création d’un compte
- Connexion avec génération de JWT
- Récupération/modification des infos perso (auth requis)

### ✅ Endpoints admin :

- Accès à la liste complète des utilisateurs
- Modification ou suppression d’utilisateurs

---

## 🧰 Repository Pattern

Tous les accès aux entités passent par un pattern **Repository** générique.

- Classe `SQLAlchemyRepository` avec héritage spécifique (`UserRepository`, `PlaceRepository`, etc.)
- Permet un découplage fort entre logique métier et ORM
- Facilite les tests et la maintenance

---

## 🧪 Base de données & scripts

- SQL scripts de création des tables
- (Optionnel) Données initiales injectables
- Utilisation de `db.create_all()` en local
- Diagrams Mermaid.js générés à partir du schéma (voir `docs/`)

---

## 🧭 Diagramme Entité-Relation

Visualisation claire de la base générée avec **Mermaid.js** :

```mermaid
erDiagram
    USER {
        string id
        string first_name
        string last_name
        string email
        string password
        boolean is_admin
    }

    PLACE {
        string id
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id
    }

    REVIEW {
        string id
        string text
        int rating
        string user_id
        string place_id
    }

    AMENITY {
        string id
        string name
    }

    PLACE_AMENITY {
        string place_id
        string amenity_id
    }

    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "has"
    PLACE ||--o{ PLACE_AMENITY : "has"
    AMENITY ||--o{ PLACE_AMENITY : "is linked with"
````
