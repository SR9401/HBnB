# Projet HbNb

Bienvenue dans notre projet collaboratif de gestion de lieux ! Cette application permet aux utilisateurs de s’inscrire, de consulter une base de lieux, d’en ajouter de nouveaux, de les filtrer selon leurs préférences et de partager des avis. Le tout est pensé pour une expérience fluide et intuitive.

---

## 🧠 Objectif du Projet

Ce projet a pour but de mettre en œuvre une application web simple et fonctionnelle autour de la découverte et du partage de lieux intéressants (sites touristiques, restaurants, spots cachés…).  
Il combine des aspects **frontend**, **backend**, et **base de données**, tout en mettant l’accent sur l’**interaction utilisateur**.

---

## ⚙️ Fonctionnalités Clés

- **Inscription / Connexion** : gestion sécurisée des comptes utilisateurs.
- **Ajout de lieux** : formulaire pour proposer de nouveaux lieux à découvrir.
- **Filtrage dynamique** : interface permettant de trier les lieux selon différents critères (popularité, type, etc).
- **Soumission d’avis** : possibilité de noter et commenter les lieux visités.
- **Visualisation interactive** : consultation facile et rapide des lieux ajoutés.

---

## 📷 Captures & Explications

### 🔹 Diagramme Général
<div align="center">
  <img src="images/Diagramme_General.png" alt="Diagramme Général" width="500"/>
</div>

Ce diagramme présente la structure logique du projet selon une architecture en couches.  
- **Couche de présentation** : gère l’affichage et la communication avec les APIs.
- **Logique métier** : applique les règles de gestion via un patron de façade pour centraliser les appels.
- **Base de données** : stockage persistant des entités (`Utilisateur`, `Lieu`, `Équipement`, `Avis`).

---

### 🔹 Diagramme de Classes
<div align="center">
  <img src="images/Diagramme_Classe.png" alt="Diagramme Mermaid" width="500"/>
</div>

Ce diagramme UML détaille les différentes entités manipulées dans l’application ainsi que leurs relations :
- `Utilisateur`, `Lieu`, `Avis`, `Équipement` sont les principales classes métier.
- Chaque entité est représentée avec ses attributs et ses associations.
- Des liens de dépendance entre les couches illustrent l’interaction des composants avec la logique métier et la base.

---

### 🔹 Enregistrement Utilisateur
<div align="center">
  <img src="images/DS_Utilisateur.png" alt="Enregistrement" width="400"/>
</div>

Diagramme de séquence décrivant le processus complet d’inscription :
- Saisie des données (email, mot de passe, pseudo) côté client.
- Vérification de format côté front.
- Transmission des données à l’API backend.
- Vérification de l’unicité, hachage du mot de passe et enregistrement en base.
- Génération d’un JWT pour authentification.
- Réponse au client indiquant le succès ou une erreur.

---

### 🔹 Soumission d’Avis
<div align="center">
  <img src="images/DS_soumission_Avis.png" alt="Soumission d’Avis" width="400"/>
</div>

Les utilisateurs peuvent évaluer un lieu en attribuant une note et en laissant un commentaire.  
Le backend valide l’authenticité de l’auteur (via token), s’assure que l’avis respecte les contraintes métiers (note entre 1 et 5, champ texte non vide) et enregistre l’avis en base.  
L’interface met ensuite à jour dynamiquement les avis affichés pour chaque lieu.

---

### 🔹 Filtrage de Lieux
<div align="center">
  <img src="images/DS_filtrage_lieux.png" alt="Filtrage" width="400"/>
</div>

L’utilisateur saisit des critères (ville, type, note).  
L’interface Web envoie la requête contenant les filtres sélectionnés à l’API backend, qui génère dynamiquement une requête SQL sécurisée.  
Les résultats sont récupérés de la base, formatés, puis renvoyés et affichés dynamiquement.  
Ce module améliore l’expérience utilisateur grâce à une recherche rapide et contextuelle.

---

## 👥 Équipe Projet

| Nom          |
|--------------|
| Ilmi Veliu   |
| Angela Rhin  |
| Rojas Shakib |

---
