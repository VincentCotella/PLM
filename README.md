
# MGO PLM System - Documentation

## Table des Matières
1. [Aperçu du Projet](#aperçu-du-projet)
2. [Structure du Projet](#structure-du-projet)
3. [Prérequis](#prérequis)
4. [Installation](#installation)
5. [Configuration de l'Environnement](#configuration-de-lenvironnement)
6. [Initialisation de la Base de Données](#initialisation-de-la-base-de-données)
7. [Lancement de l'Application](#lancement-de-lapplication)
8. [Utilisation](#utilisation)
9. [Accès à l'Interface d'Administration](#accès-à-linterface-dadministration)
10. [Fonctionnalités Implémentées](#fonctionnalités-implémentées)

---

## Aperçu du Projet
Le **MGO PLM System** est une application Django conçue pour gérer les gammes de produits et les produits individuels. Elle comprend une interface d'administration, un tableau de bord, et des formulaires pour visualiser et ajouter de nouveaux produits.

## Structure du Projet
Voici la structure de base du projet :

```
PLM/
├── plm_project/                 # Configuration principale du projet Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── products/                    # Application produits
│   ├── __init__.py
│   ├── admin.py                 # Interface d'administration
│   ├── models.py                # Modèles de données pour les produits
│   ├── views.py                 # Vues de l'application
│   ├── urls.py                  # URLs de l'application
│   ├── forms.py                 # Formulaires pour ajouter/modifier des produits
│   └── templates/               # Templates HTML
│       └── products/
│           ├── base.html        # Template de base
│           ├── dashboard.html   # Page du tableau de bord
│           ├── product_list.html# Liste des produits
│           ├── product_detail.html # Détails d'un produit
│           └── add_product.html # Formulaire pour ajouter un produit
├── initial_data.json            # Fixture JSON pour initialiser la base de données
├── db.sqlite3                   # Base de données SQLite
└── manage.py                    # Script de gestion Django
```

## Prérequis
Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- Python 3.7 ou plus récent
- Django 5.0.1
- `pip` (Python Package Installer)
- `virtualenv` (recommandé)

## Installation
Suivez ces étapes pour installer le projet localement :

1. Clonez ce dépôt :

   ```bash
   git clone https://votre-repo.git
   cd PLM
   ```

2. Créez et activez un environnement virtuel :

   ```bash
   python -m venv venv
   source venv/bin/activate   # Sur Linux/Mac
   venv\Scripts\activate    # Sur Windows
   ```

3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

## Configuration de l'Environnement
Avant de lancer le projet, ajoutez la clé secrète et configurez la base de données dans `plm_project/settings.py` si nécessaire :

```python
# plm_project/settings.py

SECRET_KEY = 'votre-clé-secrète'  # Utilisez une clé secrète pour le développement

DEBUG = True
ALLOWED_HOSTS = []
```

La base de données SQLite est configurée par défaut pour un environnement de développement local.

## Initialisation de la Base de Données
Pour initialiser la base de données avec des données de test, suivez ces étapes :

1. Appliquez les migrations pour créer la structure de la base de données :

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Créez un superutilisateur pour accéder à l'interface d'administration :

   ```bash
   python manage.py createsuperuser
   ```

3. **Initialisez la base de données avec `initial_data.json` :**

   Le fichier `initial_data.json` contient des données de base pour les gammes de produits et les produits. Pour charger ces données dans la base de données, exécutez :

   ```bash
   python manage.py loaddata initial_data.json
   ```

   ### Exemple de Contenu de `initial_data.json`
   Voici un exemple de contenu du fichier `initial_data.json` :

   ```json
   [
       {
           "model": "products.productrange",
           "pk": 1,
           "fields": {
               "name": "Agrifood Products",
               "category": "AG",
               "description": "A range of certified organic agrifood products."
           }
       },
       {
           "model": "products.productrange",
           "pk": 2,
           "fields": {
               "name": "Perfumery",
               "category": "PE",
               "description": "Exclusive collection of perfumes and cosmetics."
           }
       },
       {
           "model": "products.product",
           "pk": 1,
           "fields": {
               "reference": "AG_001",
               "name": "Organic Olive Oil",
               "product_range": 1,
               "is_modified": false,
               "created_by": 1,
               "created_at": "2024-10-03T10:00:00Z",
               "updated_at": "2024-10-03T10:00:00Z"
           }
       },
       {
           "model": "products.product",
           "pk": 2,
           "fields": {
               "reference": "PE_001",
               "name": "Luxury Perfume",
               "product_range": 2,
               "is_modified": true,
               "created_by": 1,
               "created_at": "2024-10-03T12:00:00Z",
               "updated_at": "2024-10-03T12:00:00Z"
           }
       }
   ]
   ```

4. Vérifiez que les données sont bien chargées en consultant la liste des produits dans l'interface d'administration ou sur la page d'accueil.

## Lancement de l'Application
1. Lancez le serveur de développement :

   ```bash
   python manage.py runserver
   ```

2. Ouvrez votre navigateur et accédez à :

   ```
   http://127.0.0.1:8000/
   ```

## Utilisation
- Accédez au **tableau de bord** à l'URL `http://127.0.0.1:8000/`.
- Consultez la **liste des produits** à l'URL `http://127.0.0.1:8000/products/`.
- Ajoutez de nouveaux produits via l'URL `http://127.0.0.1:8000/add/`.
- Consultez le **détail d'un produit** spécifique en accédant à `http://127.0.0.1:8000/products/<product_id>/`.

## Accès à l'Interface d'Administration
1. Connectez-vous à l'interface d'administration via :

   ```
   http://127.0.0.1:8000/admin/
   ```

2. Utilisez le nom d'utilisateur et le mot de passe du superutilisateur que vous avez créés pour vous connecter.
3. Vous pourrez alors ajouter, modifier et supprimer des produits et des gammes de produits.

## Fonctionnalités Implémentées
1. **Tableau de Bord** : Affiche le résumé des produits disponibles.
2. **Gestion des Produits** :
   - Ajouter un nouveau produit.
   - Lister tous les produits.
   - Consulter les détails d'un produit.
3. **Interface d'Administration** : Gestion des produits et des utilisateurs via l'interface d'administration Django.
4. **Authentification** :
   - Connexion.
   - Déconnexion.
   - Réinitialisation de mot de passe.

---