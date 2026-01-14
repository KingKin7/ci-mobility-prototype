# 🇨🇮 Dashboard Django - Mobilité Côte d'Ivoire

Dashboard web professionnel basé sur Django pour l'analyse des données de mobilité.

## 📋 Prérequis

- Python 3.10+
- Les données générées par le pipeline (`data/synthetic/`)

## 🚀 Installation

```bash
# Depuis le dossier racine du projet
cd src/dashboard_django

# Installer les dépendances
pip install -r requirements_django.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

## ▶️ Lancement

### Mode développement

```bash
cd src/dashboard_django
python manage.py runserver
```

Le dashboard est accessible sur : **http://localhost:8000**

### Mode production (avec Gunicorn)

```bash
cd src/dashboard_django
gunicorn wsgi:application --bind 0.0.0.0:8000
```

## 📂 Structure du projet

```
dashboard_django/
├── manage.py                 # Script de gestion Django
├── settings.py               # Configuration Django
├── urls.py                   # Routes principales
├── wsgi.py                   # Point d'entrée WSGI
├── requirements_django.txt   # Dépendances
│
├── api/                      # API REST
│   ├── views.py             # Endpoints API
│   └── urls.py              # Routes API
│
├── dashboard_app/            # Application Dashboard
│   ├── views.py             # Vues Django
│   ├── urls.py              # Routes pages
│   ├── templates/           # Templates HTML
│   │   └── dashboard/
│   │       ├── base.html
│   │       ├── overview.html
│   │       ├── poverty.html
│   │       ├── migration.html
│   │       ├── mobility.html
│   │       └── map.html
│   └── static/              # Fichiers statiques
│       └── dashboard/
│           ├── css/style.css
│           └── js/main.js
│
└── services/                 # Couche métier
    └── data_service.py      # Chargement et traitement des données
```

## 🌐 Pages disponibles

| URL | Description |
|-----|-------------|
| `/` | Vue d'ensemble |
| `/poverty/` | Analyse de la pauvreté |
| `/migration/` | Analyse des migrations |
| `/mobility/` | Analyse de la mobilité et congestion |
| `/map/` | Carte interactive |

## 🔌 API REST

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/overview/` | GET | Statistiques générales |
| `/api/poverty/` | GET | Données de pauvreté |
| `/api/migration/` | GET | Données de migration |
| `/api/mobility/` | GET | Données de mobilité |
| `/api/map/` | GET | Données cartographiques |
| `/api/dataset/<name>/` | GET | Dataset brut (users, poverty, migration, mobility) |
| `/api/refresh/` | POST | Rafraîchir le cache |

### Exemple d'utilisation de l'API

```python
import requests

# Récupérer les statistiques de pauvreté
response = requests.get('http://localhost:8000/api/poverty/')
data = response.json()
print(f"Taux de pauvreté: {data['poverty_rate']}%")
```

## 🛠️ Technologies utilisées

### Backend
- **Django 4.2** - Framework web Python
- **Django REST Framework** - API REST
- **Pandas** - Traitement des données

### Frontend
- **Bootstrap 5** - Framework CSS
- **Chart.js** - Graphiques interactifs
- **Plotly.js** - Visualisations avancées (heatmaps, scatter plots)
- **Leaflet** - Cartes interactives

## ⚙️ Configuration

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `DJANGO_SECRET_KEY` | Clé secrète Django | dev-key |
| `DJANGO_DEBUG` | Mode debug | True |

### Fichier settings.py

Le chemin des données est configuré dans `DATA_DIR`:

```python
DATA_DIR = BASE_DIR.parent.parent / 'data' / 'synthetic'
```

## 📊 Comparaison avec Streamlit

| Aspect | Streamlit | Django |
|--------|-----------|--------|
| Déploiement | Simple (Streamlit Cloud) | Standard (Docker, VM, etc.) |
| Personnalisation | Limitée | Totale |
| API REST | Non | Oui |
| Performance | Correcte | Optimisée |
| Multi-utilisateurs | Limité | Natif |
| Authentification | Plugin | Intégrée |

## 🔒 Sécurité (Production)

Pour un déploiement en production :

1. Générer une clé secrète :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

2. Configurer les variables d'environnement :
```bash
export DJANGO_SECRET_KEY="votre-cle-secrete"
export DJANGO_DEBUG="False"
```

3. Configurer `ALLOWED_HOSTS` dans settings.py

## 📝 Licence

Projet ANStat - DataLab - Standard UN-MPDMS v2.0

---

**© 2026 ANStat - DataLab**
