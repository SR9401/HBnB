# HBnB – Phase 2

## 🎯 Objectif du projet

Créer une API REST pour gérer les entités principales d’un système de location de logements (type Airbnb) avec Flask‑RESTx, en séparant clairement :

- la couche de présentation (API),
- la logique métier (Facade),
- et la persistance (repository).

Le projet repose sur la validation stricte des données, la modélisation claire des entités, la documentation automatique Swagger, et des tests unitaires couvrant tous les cas.

---

## 📁 Structure du projet

part2/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── amenities.py
│   │       └── reviews.py
│   ├── models/
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── amenity.py
│   │   └── review.py
│   ├── services/
│   │   └── facade.py
│   └── persistence/
│       └── repository.py
├── run.py
├── config.py
├── requirements.txt
└── test/
    ├── test_amenity_api.py
    ├── test_place_api.py
    ├── test_review_api.py
    └── test_user_api.py


---

## 📦 Installation des dépendances

Pour installer les paquets nécessaires, exécute la commande suivante dans le terminal :

bash
pip install -r requirements.txt


---

## 🧠 Couche de logique métier

Cette couche est responsable de toutes les règles de validation et du fonctionnement interne de la plateforme.  
Elle est **indépendante** de l'API (Flask) et de la persistance (repository), ce qui garantit une **meilleure modularité, testabilité et clarté** du code.

---

## Entités et leurs responsabilités

### 🧍‍♂️ User

Représente un utilisateur inscrit sur la plateforme.

**Attributs** :

- id (str) : identifiant unique  
- first_name (str) : prénom (obligatoire, 50 caractères max)  
- last_name (str) : nom (obligatoire, 50 caractères max)  
- email (str) : adresse email valide et unique  
- is_admin (bool) : rôle administrateur (valeur par défaut : False)  
- created_at / updated_at (datetime)

**Responsabilités** :

- Gérer les informations personnelles  
- Vérifier la validité et l’unicité de l’email  
- Identifier les utilisateurs administrateurs  
- Être lié à des lieux (Place) et des avis (Review)

**Exemple d'utilisation** :

python
user = User(
    id="u001",
    first_name="Leïla",
    last_name="Durand",
    email="leila@example.com"
)
print(user.email)      # leila@example.com
print(user.is_admin)   # False


---

### 🏠 Place

Représente un lieu proposé à la location.

**Attributs** :

- id (str) : identifiant unique  
- title (str) : titre (obligatoire, 100 caractères max)  
- description (str) : description du logement  
- price (float) : prix par nuit (positif)  
- latitude / longitude (float) : coordonnées géographiques  
- owner (User) : utilisateur propriétaire du lieu  
- created_at / updated_at (datetime)

**Responsabilités** :

- Valider les coordonnées géographiques et le prix  
- Être associé à un utilisateur valide  
- Être listé, filtré ou noté

**Exemple d'utilisation** :

python
place = Place(
    id="p002",
    title="Maison de campagne",
    description="Idéale pour un week-end au calme.",
    price=110.0,
    latitude=44.9333,
    longitude=1.2667,
    owner=user
)
print(place.title)     # Maison de campagne
print(place.price)     # 110.0


---

### ⭐ Review

Représente l’avis laissé par un utilisateur sur un lieu.

**Attributs** :

- id (str) : identifiant unique  
- text (str) : contenu de l’avis (obligatoire)  
- rating (int) : note de 1 à 5  
- place (Place) : lieu concerné  
- user (User) : auteur de l’avis  
- created_at / updated_at (datetime)

**Responsabilités** :

- Valider que la note est entre 1 et 5  
- Être lié à un utilisateur et un lieu existants  
- Contribuer à la réputation d’un lieu

**Exemple d'utilisation** :

python
review = Review(
    id="r001",
    text="Très bon rapport qualité/prix.",
    rating=4,
    place=place,
    user=user
)
print(review.rating)         # 4
print(review.place.title)    # Maison de campagne


---

### 🛏️ Amenity

Représente un équipement ou un service disponible dans un logement (ex : Wi-Fi, Parking…).

**Attributs** :

- id (str) : identifiant unique  
- name (str) : nom de l’équipement (obligatoire, max. 50 caractères)  
- created_at / updated_at (datetime)

**Responsabilités** :

- Être lié à un ou plusieurs lieux (Place)  
- Permettre le filtrage de lieux par équipements

**Exemple d'utilisation** :

python
wifi = Amenity(id="b566", name="Wi-Fi")
print(wifi.name)  # Wi-Fi

## 👥 Contributeurs

- **Angela Rhin**
- **Shakib Rojas**
- **Ilmi Veliu**

Merci à tous pour votre travail et votre collaboration sur ce projet HBnB – Phase 2.