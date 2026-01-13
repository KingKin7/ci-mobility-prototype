# 🇨🇮 Pipeline Données de Téléphonie Mobile - ANStat

## Prototype pour l'analyse de la mobilité en Côte d'Ivoire

Ce projet implémente un pipeline complet de génération et d'analyse de données synthétiques de téléphonie mobile, conformément aux standards des Nations Unies (UN-MPDMS/MPDMIS).

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Standard UN-MPDMS](https://img.shields.io/badge/standard-UN--MPDMS%20v2.0-green.svg)](https://unstats.un.org/)
[![Streamlit Dashboard](https://img.shields.io/badge/dashboard-Streamlit-red.svg)](https://streamlit.io/)

## 📊 Objectifs du Projet

Le prototype couvre trois axes d'analyse principaux :

1. **Analyse de la Pauvreté** - Estimation des indicateurs socio-économiques via indices de richesse (PCA, Alkire-Foster)
2. **Analyse de la Migration** - Détection des flux migratoires internes (permanents, saisonniers, pendulaires)
3. **Analyse de la Mobilité** - Étude des déplacements quotidiens et matrices Origine-Destination

## 🏗️ Structure du Projet

```
ci-mobility-prototype/
├── config/                     # Configuration
│   └── data_params.yml        # Paramètres de génération
├── src/                       # Code source
│   ├── data_generation/       # Génération de données synthétiques
│   │   └── synthetic_generator.py
│   ├── indicators/            # Calcul des indicateurs
│   │   ├── poverty_index.py   # Indice de pauvreté (PCA, quintiles, IPM)
│   │   ├── migration_flows.py # Flux migratoires et statistiques
│   │   └── mobility_metrics.py # Métriques de mobilité (OD, accessibilité)
│   ├── pipeline/              # Orchestration
│   │   └── run_pipeline.py    # Pipeline principal (6 étapes)
│   ├── api/                   # API REST (FastAPI)
│   ├── dashboard/             # Dashboard interactif
│   │   └── app.py             # Application Streamlit
│   ├── privacy/               # Anonymisation et confidentialité
│   ├── utils/                 # Utilitaires communs
│   └── validation/            # Validation des données
├── data/                      # Données
│   ├── raw/                   # Données brutes (GADM boundaries)
│   │   └── gadm41_CIV_4.json  # Limites administratives Côte d'Ivoire
│   ├── processed/             # Données traitées et enrichies
│   │   ├── exploration/       # Aperçus des données
│   │   ├── stats/             # Statistiques exportées
│   │   └── figures/           # Visualisations
│   ├── synthetic/             # Données synthétiques générées
│   └── metadata/              # Métadonnées des datasets
├── notebooks/                 # Notebooks Jupyter
│   └── 01_exploration_donnees.ipynb  # Exploration interactive
├── tests/                     # Tests unitaires
├── docs/                      # Documentation
├── logs/                      # Fichiers de log
├── requirements.txt           # Dépendances Python
└── pyproject.toml             # Configuration du projet
```

## 🚀 Installation

### Prérequis

- Python 3.9+
- pip ou conda
- Git

### Installation rapide

```bash
# Cloner le repository
git clone <repository-url>
cd ci-mobility-prototype

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows (CMD)
.\venv\Scripts\Activate   # Windows (PowerShell)

# Installer les dépendances
pip install -r requirements.txt
```

### Vérification de l'installation

```bash
# Vérifier que tout est installé
python -c "import pandas, geopandas, streamlit, h3; print('✅ Installation OK')"
```

## 📖 Utilisation

### 1. Exécuter le pipeline complet

```bash
python -m src.pipeline.run_pipeline
```

Le pipeline exécute 6 étapes :
1. **Génération** - Création des données synthétiques (users, poverty, migration, mobility)
2. **Indicateurs** - Calcul des indices de pauvreté, migration et mobilité
3. **Enrichissement** - Ajout des métadonnées et géolocalisation
4. **Agrégation** - Agrégation spatiale et temporelle
5. **Export** - Sauvegarde des résultats (CSV, JSON, YAML)
6. **Rapport** - Génération du rapport de synthèse

### 2. Lancer le dashboard interactif

```bash
streamlit run src/dashboard/app.py
```

Le dashboard offre :
- 🗺️ **Cartes interactives** - Visualisation géographique des indicateurs
- 📊 **Analyse de pauvreté** - Distribution des quintiles et IPM
- 🚶 **Flux migratoires** - Corridors et statistiques de migration
- 🚗 **Mobilité** - Matrices OD et répartition modale

### 3. Explorer les données (Notebook)

```bash
jupyter notebook notebooks/01_exploration_donnees.ipynb
```

### 4. Générer uniquement les données

```bash
python -m src.data_generation.synthetic_generator
```

### 5. Calculer les indicateurs séparément

```python
from src.indicators.poverty_index import PovertyIndexCalculator
from src.indicators.migration_flows import MigrationDetector
from src.indicators.mobility_metrics import MobilityAnalyzer

# Pauvreté
calculator = PovertyIndexCalculator()
df_result, stats = calculator.process(poverty_data)

# Migration
detector = MigrationDetector()
migration_df, migration_stats = detector.process(migration_data)

# Mobilité
analyzer = MobilityAnalyzer()
mobility_df, mobility_stats = analyzer.process(mobility_data)
```

### Options de la ligne de commande

```bash
# Voir l'aide
python -m src.pipeline.run_pipeline --help

# Ne pas sauvegarder les fichiers
python -m src.pipeline.run_pipeline --no-save

# Utiliser une configuration personnalisée
python -m src.pipeline.run_pipeline --config path/to/config.yml

# Exécuter une seule étape
python -m src.pipeline.run_pipeline --step 1  # Génération uniquement
```

## 📈 Datasets Générés

### 1. Profils Utilisateurs (`users`) - ~10,000 enregistrements
| Colonne | Description |
|---------|-------------|
| `user_id` | Identifiant anonymisé (SHA-256) |
| `age_group` | Groupe d'âge (18-25, 26-35, etc.) |
| `gender` | Genre (M/F) |
| `occupation` | Catégorie professionnelle |
| `phone_type` | Type de téléphone (basic, feature, smartphone) |
| `locality` / `region` | Localisation administrative |
| `home_lat` / `home_lon` | Coordonnées du domicile |
| `home_h3` | Cellule H3 (résolution 7) |
| `urban_rural` | Zone urbaine ou rurale |

### 2. Données de Pauvreté (`poverty`) - ~50,000 enregistrements
| Colonne | Description |
|---------|-------------|
| `recharge_amount_fcfa` | Montant de recharge (FCFA) |
| `recharge_frequency_weekly` | Fréquence hebdomadaire |
| `call_duration_sec` | Durée d'appel (secondes) |
| `data_mb` | Consommation data (Mo) |
| `contact_diversity_score` | Score de diversité des contacts |
| `mobility_radius_km` | Rayon de mobilité (km) |

### 3. Données de Migration (`migration`) - ~500 événements
| Colonne | Description |
|---------|-------------|
| `origin_locality` / `origin_region` | Origine |
| `current_locality` / `current_region` | Destination |
| `movement_type` | Type (permanent, seasonal, return, pendular) |
| `residence_duration_days` | Durée de résidence |
| `distance_km` | Distance parcourue |
| `is_return_migration` | Migration de retour (bool) |

### 4. Données de Mobilité (`mobility`) - ~17,000 trajets
| Colonne | Description |
|---------|-------------|
| `origin_h3` / `destination_h3` | Cellules H3 O/D |
| `transport_mode` | Mode (walk, car, bus, moto, gbaka) |
| `trip_purpose` | Motif (work, shopping, leisure, etc.) |
| `distance_km` | Distance (km) |
| `duration_min` | Durée (minutes) |
| `hour_of_day` | Heure de départ |

## 🔬 Indicateurs Calculés

### Pauvreté
| Indicateur | Méthode | Description |
|------------|---------|-------------|
| Indice de richesse | PCA | Analyse en composantes principales sur les features téléphonie |
| Quintiles de richesse | Quantiles | Classification en 5 groupes (Q1=plus pauvre) |
| IPM (Indice de Pauvreté Multidimensionnel) | Alkire-Foster | Score de privation (0-1) |
| Taux de pauvreté | Seuil k=0.33 | % population en pauvreté multidimensionnelle |

### Migration
| Indicateur | Description |
|------------|-------------|
| Taux de migration interne | % utilisateurs ayant migré |
| Flux nets par zone | Entrées - Sorties par région |
| Distance moyenne | Distance moyenne de migration (km) |
| Distribution par type | Répartition permanent/saisonnier/pendulaire |

### Mobilité
| Indicateur | Description |
|------------|-------------|
| Matrice Origine-Destination | Flux entre cellules H3 |
| Répartition modale | % par mode de transport |
| Temps de trajet moyen | Durée moyenne des déplacements |
| Distribution horaire | Heures de pointe (matin/soir) |
| Accessibilité (SDG 11.2.1) | Accès aux transports publics |

## ⚙️ Configuration

Le fichier `config/data_params.yml` permet de personnaliser :

```yaml
# Paramètres principaux
n_users: 10000              # Nombre d'utilisateurs
days: 365                   # Période de simulation (jours)
random_seed: 42             # Graine aléatoire

# Distribution géographique (191 localités GADM)
# Basé sur gadm41_CIV_4.json (limites administratives niveau 4)

# Paramètres de mobilité
mobility_sample_ratio: 0.1  # % utilisateurs avec données mobilité
trips_per_user: [10, 30]    # Plage de trajets par utilisateur

# Paramètres de migration
migration_rate: 0.05        # Taux de migration (~5%)
```

## 🖥️ Dashboard

Le dashboard Streamlit (`src/dashboard/app.py`) offre une interface interactive :

### Fonctionnalités
- **Vue d'ensemble** : Métriques clés et résumé des données
- **Analyse de pauvreté** : Carte des quintiles, distribution IPM
- **Analyse de migration** : Flux migratoires, corridors principaux
- **Analyse de mobilité** : Matrices OD, heures de pointe
- **Export** : Téléchargement des données filtrées

### Lancement
```bash
streamlit run src/dashboard/app.py
# Accessible sur http://localhost:8501
```

## 🛠️ Développement

### Extensions VSCode recommandées

| Extension | ID | Description |
|-----------|----|----|
| Python | ms-python.python | Support Python |
| Pylance | ms-python.vscode-pylance | IntelliSense avancé |
| GitHub Copilot | github.copilot | Assistance IA |
| Jupyter | ms-toolsai.jupyter | Support notebooks |
| GitLens | eamodio.gitlens | Historique Git |

### Fichier `.vscode/settings.json` suggéré

```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.analysis.typeCheckingMode": "basic",
    "python.formatting.provider": "none",
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
    },
    "python.linting.enabled": true
}
```

### Tests

```bash
# Exécuter tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=src --cov-report=html
```

### Qualité du code

```bash
# Formatage
black src/

# Linting
flake8 src/

# Type checking
mypy src/
```

## 📋 Conformité aux Standards

Ce projet respecte les guidelines suivants :

| Standard | Description |
|----------|-------------|
| **UN-MPDMS** | Mobile Positioning Data for Migration Statistics |
| **UN-MPDMIS** | Mobile Positioning Data for Mobility and Infrastructure Statistics |
| **GDPR** | Protection des données et anonymisation |
| **k-Anonymité** | Minimum de 10 utilisateurs par groupe |
| **SDG 11.2.1** | Indicateur d'accessibilité aux transports |

## 🔒 Protection de la Vie Privée

| Mesure | Implémentation |
|--------|----------------|
| Anonymisation | Hachage SHA-256 des identifiants |
| Agrégation | Minimum 10 utilisateurs par groupe |
| Géolocalisation | Cellules H3 résolution 7 (~5km²) |
| Confidentialité différentielle | Support ε = 1.0 (optionnel) |
| Rotation des sels | Sels d'anonymisation rotatifs |

## 📦 Dépendances Principales

```
pandas>=2.0.0          # Manipulation des données
geopandas>=0.14.0      # Données géospatiales
h3>=4.0.0              # Indexation spatiale H3
scikit-learn>=1.0.0    # Machine learning (PCA)
streamlit>=1.20.0      # Dashboard interactif
plotly>=5.0.0          # Visualisations
folium>=0.14.0         # Cartes interactives
loguru>=0.7.0          # Logging
pyyaml>=6.0            # Configuration YAML
```

## 📚 Documentation Supplémentaire

- [Notebook d'exploration](notebooks/01_exploration_donnees.ipynb) - Exploration interactive des données
- [Configuration](config/data_params.yml) - Paramètres de génération
- Dossier `docs/` - Documentation technique détaillée

## 🐛 Dépannage

### Erreurs courantes

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError: h3` | `pip install h3` |
| `FileNotFoundError: gadm41_CIV_4.json` | Télécharger les limites GADM dans `data/raw/` |
| Dashboard qui clignote | Utiliser `st.cache_data` et paramètre `key` |
| `numpy.int64` dans `timedelta` | Convertir avec `int()` |

### Logs

Les logs sont générés dans le dossier `logs/` et affichés dans la console avec Loguru.

## 🤝 Contribution

Les contributions sont les bienvenues ! Merci de :

1. Forker le repository
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalité`)
3. Commiter vos changements (`git commit -m 'Ajout de...'`)
4. Pousser la branche (`git push origin feature/nouvelle-fonctionnalité`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est développé dans le cadre des activités de l'ANStat (Agence Nationale de la Statistique) de Côte d'Ivoire.

## 📞 Contact

Pour toute question concernant ce projet, contactez l'équipe DataLab de l'ANStat.

---

**Version**: 1.0.0  
**Standard**: UN-MPDMS/MPDMIS v2.0  
**Dernière mise à jour**: Janvier 2026  
**Python**: 3.9+
