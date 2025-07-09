# README
# 🏠 HBnB - Airbnb Clone

HBnB est un clone simplifié d'Airbnb conçu pour offrir une plateforme de réservation entre utilisateurs et hôtes. Ce projet est un exercice d’architecture logicielle combinant **backend Python**, **stockage de données relationnel** et **visualisation de structure** via **Mermaid.js**.

## 🚀 Fonctionnalités

- Création de comptes utilisateurs avec rôles
- Ajout de logements (`Place`) avec coordonnées, prix, et description
- Ajout d’équipements (`Amenity`) associés aux logements
- Publication de critiques (`Review`) pour les logements
- Système de réservation (optionnel)
- Visualisation claire de la base de données avec diagramme ER

---

## 🗂️ Structure de la base de données

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

    RESERVATION {
        string id
        date start_date
        date end_date
        string user_id
        string place_id
    }

    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    USER ||--o{ RESERVATION : "makes"
    PLACE ||--o{ REVIEW : "has"
    PLACE ||--o{ PLACE_AMENITY : "has"
    PLACE ||--o{ RESERVATION : "booked in"
    AMENITY ||--o{ PLACE_AMENITY : "is linked with"
````

🧰 Technologies
Python 3.x
SQLAlchemy (ORM)
MySQL / SQLite
Mermaid.js (pour le diagramme)
Git / GitHub

⚙️ Installation
```bash
git clone https://github.com/ton-utilisateur/hbnb.git
cd hbnb
pip install -r requirements.txt
````

📸 Exemple d'utilisation

1. Créer un utilisateur
2. Ajouter un logement
3. Lier des équipements
4. Poster une review
5. Faire une réservation (si activé)

✍️ Auteurs
Angela RHIN
Shakib ROJAS