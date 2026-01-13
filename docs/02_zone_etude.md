# 3. Description des Données

---

## 3.1 Vue d'ensemble

### 3.1.1 Sources de données

Ce projet utilise des **données synthétiques** générées pour simuler des Call Detail Records (CDR) de téléphonie mobile. Ces données sont calibrées sur les statistiques officielles de la Côte d'Ivoire.

| Source | Type | Utilisation |
|--------|------|-------------|
| RGPH 2021 | Officielle | Calibration démographique |
| ENV 2018 | Officielle | Calibration pauvreté |
| GADM v4.1 | Géographique | Limites administratives |
| Générateur synthétique | Simulée | Données d'analyse |

### 3.1.2 Datasets générés

Le pipeline génère **4 datasets** interconnectés :

| Dataset | Description | Volume | Période |
|---------|-------------|--------|---------|
| `users` | Profils des utilisateurs | 10 000 | - |
| `poverty` | Indicateurs de pauvreté | 50 000 | 5 mois |
| `migration` | Événements de migration | 500 | 12 mois |
| `mobility` | Trajets quotidiens | ~17 000 | 30 jours |

### 3.1.3 Schéma relationnel

---

## 3.2 Dataset USERS (Profils utilisateurs)

### 3.2.1 Description

Le dataset `users` contient les **profils démographiques et comportementaux** des utilisateurs de téléphonie mobile simulés.

| Caractéristique | Valeur |
|-----------------|--------|
| Nombre d'enregistrements | 10 000 |
| Nombre de colonnes | 15 |
| Clé primaire | `user_id` |
| Granularité | 1 ligne par utilisateur |

### 3.2.2 Dictionnaire des variables

| Variable | Type | Description | Exemple |
|----------|------|-------------|---------|
| `user_id` | string | Identifiant unique anonymisé | "USR_00001" |
| `age_group` | string | Tranche d'âge | "25-34" |
| `gender` | string | Genre (M/F) | "F" |
| `locality` | string | Localité de résidence | "Adjamé" |
| `region` | string | Région administrative | "Abidjan" |
| `district` | string | District | "Abidjan" |
| `urban_rural` | string | Type de zone | "urban" |
| `home_lat` | float | Latitude du domicile | 5.3364 |
| `home_lon` | float | Longitude du domicile | -4.0267 |
| `home_h3` | string | Cellule H3 du domicile (résolution 7) | "872a1072bffffff" |
| `phone_type` | string | Type de téléphone | "smartphone" |
| `operator` | string | Opérateur télécom | "Orange" |
| `subscription_type` | string | Type d'abonnement | "prepaid" |
| `activity_level` | string | Niveau d'activité téléphonique | "high" |
| `registration_date` | date | Date d'inscription simulée | "2024-03-15" |

### 3.2.3 Distributions

**Répartition par genre** :
| Genre | Nombre | Pourcentage |
|-------|--------|-------------|
| Masculin | 5 120 | 51.2% |
| Féminin | 4 880 | 48.8% |

**Répartition par groupe d'âge** :
| Groupe | Nombre | Pourcentage |
|--------|--------|-------------|
| 15-24 | 2 850 | 28.5% |
| 25-34 | 2 660 | 26.6% |
| 35-44 | 1 980 | 19.8% |
| 45-54 | 1 350 | 13.5% |
| 55-64 | 780 | 7.8% |
| 65+ | 380 | 3.8% |

**Répartition urbain/rural** :
| Zone | Nombre | Pourcentage |
|------|--------|-------------|
| Urbain | 5 490 | 54.9% |
| Rural | 4 510 | 45.1% |

### 3.2.4 Qualité des données

| Indicateur | Valeur |
|------------|--------|
| Complétude | 100% |
| Unicité user_id | 100% |
| Coordonnées valides | 99.8% |

---

## 3.3 Dataset POVERTY (Indicateurs de pauvreté)

### 3.3.1 Description

Le dataset `poverty` contient les **indicateurs comportementaux** utilisés pour estimer la pauvreté, avec une observation par utilisateur et par mois.

| Caractéristique | Valeur |
|-----------------|--------|
| Nombre d'enregistrements | 50 000 |
| Nombre de colonnes | 18 |
| Clé primaire | (`user_id`, `month`) |
| Granularité | 1 ligne par utilisateur par mois |

### 3.3.2 Dictionnaire des variables

| Variable | Type | Description | Unité | Exemple |
|----------|------|-------------|-------|---------|
| `user_id` | string | Identifiant utilisateur | - | "USR_00001" |
| `month` | string | Mois d'observation | YYYY-MM | "2025-08" |
| `region` | string | Région de résidence | - | "Abidjan" |
| `urban_rural` | string | Type de zone | - | "urban" |
| `recharge_amount_fcfa` | float | Montant total des recharges | FCFA | 15000 |
| `recharge_frequency_weekly` | float | Fréquence de recharge | par semaine | 2.5 |
| `call_duration_sec` | float | Durée totale des appels | secondes | 3600 |
| `sms_count` | int | Nombre de SMS envoyés | - | 45 |
| `data_mb` | float | Consommation data | Mo | 512.5 |
| `unique_contacts` | int | Nombre de contacts uniques | - | 28 |
| `contact_diversity_score` | float | Score de diversité des contacts | 0-1 | 0.72 |
| `mobility_radius_km` | float | Rayon de mobilité mensuel | km | 12.5 |
| `night_activity_ratio` | float | Ratio activité nocturne | 0-1 | 0.15 |
| `weekend_activity_ratio` | float | Ratio activité weekend | 0-1 | 0.35 |
| `international_calls` | int | Nombre d'appels internationaux | - | 3 |
| `top_up_regularity` | float | Régularité des recharges | 0-1 | 0.85 |
| `device_change_count` | int | Changements d'appareil | - | 0 |
| `antenna_diversity` | int | Nombre d'antennes utilisées | - | 15 |

### 3.3.3 Variables calculées (post-traitement)

Ces variables sont ajoutées par le module `poverty_index.py` :

| Variable | Type | Description | Méthode |
|----------|------|-------------|---------|
| `wealth_index` | float | Indice de richesse | PCA |
| `wealth_quintile` | int | Quintile de richesse (1-5) | Quantiles |
| `mpi_score` | float | Score IPM | Alkire-Foster |
| `is_mpi_poor` | bool | Pauvre selon IPM | Seuil 0.33 |

### 3.3.4 Statistiques descriptives

| Variable | Moyenne | Écart-type | Min | Max |
|----------|---------|------------|-----|-----|
| recharge_amount_fcfa | 12 450 | 8 320 | 500 | 75 000 |
| call_duration_sec | 2 840 | 2 150 | 0 | 18 000 |
| data_mb | 385 | 520 | 0 | 5 000 |
| mobility_radius_km | 8.5 | 12.3 | 0.1 | 150 |
| contact_diversity_score | 0.58 | 0.22 | 0 | 1 |

---

## 3.4 Dataset MIGRATION (Événements de migration)

### 3.4.1 Description

Le dataset `migration` contient les **événements de migration détectés**, correspondant à des changements de résidence significatifs.

| Caractéristique | Valeur |
|-----------------|--------|
| Nombre d'enregistrements | ~500 |
| Nombre de colonnes | 15 |
| Clé primaire | (`user_id`, `timestamp`) |
| Granularité | 1 ligne par événement de migration |

### 3.4.2 Dictionnaire des variables

| Variable | Type | Description | Exemple |
|----------|------|-------------|---------|
| `user_id` | string | Identifiant utilisateur | "USR_00234" |
| `timestamp` | datetime | Date de détection | "2025-06-15" |
| `origin_locality` | string | Localité d'origine | "Bouaké" |
| `origin_region` | string | Région d'origine | "Gbêkê" |
| `origin_lat` | float | Latitude origine | 7.6906 |
| `origin_lon` | float | Longitude origine | -5.0308 |
| `current_locality` | string | Localité destination | "Abidjan" |
| `current_region` | string | Région destination | "Abidjan" |
| `current_lat` | float | Latitude destination | 5.3364 |
| `current_lon` | float | Longitude destination | -4.0267 |
| `distance_km` | float | Distance parcourue | 348.5 |
| `residence_duration_days` | int | Durée à la nouvelle résidence | 45 |
| `movement_type` | string | Type de migration | "long_distance" |
| `is_return_migration` | bool | Migration de retour | False |
| `previous_locations` | list | Historique des localisations | ["Korhogo", "Bouaké"] |

### 3.4.3 Types de migration (classification UN-MPDMS)

| Type | Définition | Critères |
|------|------------|----------|
| `long_distance` | Migration longue distance | Distance > 200 km |
| `regional` | Migration régionale | 50 km < Distance ≤ 200 km |
| `local` | Migration locale | Distance ≤ 50 km |
| `return` | Migration de retour | Retour lieu d'origine |
| `seasonal` | Migration saisonnière | Durée < 6 mois, pattern répétitif |
| `circular` | Migration circulaire | Mouvements répétés entre 2+ lieux |

### 3.4.4 Statistiques

| Indicateur | Valeur |
|------------|--------|
| Nombre total de migrations | ~500 |
| Distance moyenne | 125.4 km |
| Distance médiane | 85.2 km |
| Durée moyenne séjour | 68 jours |
| Taux de migration retour | 15.2% |

**Répartition par type** :
| Type | Nombre | Pourcentage |
|------|--------|-------------|
| long_distance | 95 | 19% |
| regional | 180 | 36% |
| local | 125 | 25% |
| return | 55 | 11% |
| seasonal | 45 | 9% |

---

## 3.5 Dataset MOBILITY (Trajets quotidiens)

### 3.5.1 Description

Le dataset `mobility` contient les **trajets quotidiens** des utilisateurs, représentant leurs déplacements au cours d'une période de 30 jours.

| Caractéristique | Valeur |
|-----------------|--------|
| Nombre d'enregistrements | ~17 000 |
| Nombre de colonnes | 18 |
| Clé primaire | (`user_id`, `timestamp`) |
| Granularité | 1 ligne par trajet |

### 3.5.2 Dictionnaire des variables

| Variable | Type | Description | Exemple |
|----------|------|-------------|---------|
| `user_id` | string | Identifiant utilisateur | "USR_00001" |
| `timestamp` | datetime | Date et heure du trajet | "2025-09-15 08:30:00" |
| `origin_h3` | string | Cellule H3 origine | "872a1072bffffff" |
| `destination_h3` | string | Cellule H3 destination | "872a1073affffff" |
| `origin_lat` | float | Latitude origine | 5.3364 |
| `origin_lon` | float | Longitude origine | -4.0267 |
| `destination_lat` | float | Latitude destination | 5.3512 |
| `destination_lon` | float | Longitude destination | -4.0089 |
| `distance_km` | float | Distance du trajet | 3.5 |
| `duration_min` | float | Durée du trajet | 25.0 |
| `speed_kmh` | float | Vitesse moyenne | 8.4 |
| `transport_mode` | string | Mode de transport inféré | "bus" |
| `trip_purpose` | string | Motif du déplacement | "work" |
| `day_of_week` | int | Jour de la semaine (0-6) | 1 |
| `hour_of_day` | int | Heure du départ (0-23) | 8 |
| `is_peak_hour` | bool | Heure de pointe | True |
| `origin_poi_type` | string | Type de POI origine | "residential" |
| `destination_poi_type` | string | Type de POI destination | "commercial" |

### 3.5.3 Modes de transport

| Mode | Vitesse typique | Critères d'inférence |
|------|-----------------|---------------------|
| `walk` | < 6 km/h | Courte distance, faible vitesse |
| `bicycle` | 6-15 km/h | Distance moyenne, vitesse modérée |
| `bus` | 10-25 km/h | Pattern horaire, arrêts fréquents |
| `taxi` | 15-40 km/h | Trajet direct, vitesse variable |
| `car` | 20-60 km/h | Trajet direct, vitesse élevée |

### 3.5.4 Motifs de déplacement

| Motif | Description | Heures typiques |
|-------|-------------|-----------------|
| `home` | Retour au domicile | Soir, nuit |
| `work` | Trajet domicile-travail | 6h-9h, 17h-20h |
| `education` | École, université | 7h-8h, 12h, 16h-17h |
| `shopping` | Achats, marché | 9h-12h, 15h-18h |
| `leisure` | Loisirs, visites | Weekend, soirées |
| `health` | Santé | Variable |
| `other` | Autre | Variable |

### 3.5.5 Statistiques

| Indicateur | Valeur |
|------------|--------|
| Trajets par utilisateur | 16.9 (moyenne) |
| Distance moyenne | 5.8 km |
| Durée moyenne | 28.5 min |
| Vitesse moyenne | 12.2 km/h |

**Distribution horaire** :
| Période | Pourcentage |
|---------|-------------|
| Nuit (0h-6h) | 5% |
| Matin (6h-12h) | 35% |
| Après-midi (12h-18h) | 40% |
| Soir (18h-24h) | 20% |

---

## 3.6 Données géographiques (GADM)

### 3.6.1 Source

Les limites administratives proviennent de la base **GADM version 4.1** (Global Administrative Areas Database).

| Fichier | Format | Contenu |
|---------|--------|---------|
| `gadm41_CIV_4.json` | GeoJSON | Limites niveau 4 (sous-préfectures) |

### 3.6.2 Structure

| Niveau | Champ | Nombre d'entités |
|--------|-------|------------------|
| ADM0 | COUNTRY | 1 |
| ADM1 | NAME_1 | 14 (districts) |
| ADM2 | NAME_2 | 31 (régions) |
| ADM3 | NAME_3 | 108 (départements) |
| ADM4 | NAME_4 | 510 (sous-préfectures) |

### 3.6.3 Utilisation

- **Agrégation spatiale** : Résultats par région/district
- **Génération** : Attribution des localités aux utilisateurs
- **Visualisation** : Cartes choroplèthes

---

## 3.7 Indexation spatiale H3

### 3.7.1 Système H3

Le projet utilise le système d'indexation **H3** (Uber) pour la discrétisation spatiale :

| Caractéristique | Valeur |
|-----------------|--------|
| Géométrie | Hexagones |
| Résolution utilisée | 7 |
| Surface par cellule | ~5.16 km² |
| Nombre de cellules CI | ~62 500 |

### 3.7.2 Avantages de H3

| Avantage | Description |
|----------|-------------|
| **Uniformité** | Cellules de surface égale |
| **Voisinage** | 6 voisins à chaque cellule |
| **Hiérarchie** | Agrégation multi-résolution |
| **Performance** | Indexation O(1) |
| **Anonymisation** | Masquage des positions exactes |

### 3.7.3 Résolutions disponibles

| Résolution | Surface | Utilisation |
|------------|---------|-------------|
| 5 | ~252 km² | Niveau régional |
| 6 | ~36 km² | Niveau département |
| 7 | ~5.16 km² | Niveau commune |
| 8 | ~0.74 km² | Niveau quartier |
| 9 | ~0.11 km² | Niveau rue |

---

## 3.8 Qualité des données

### 3.8.1 Contrôles de qualité

| Contrôle | Dataset | Résultat |
|----------|---------|----------|
| Unicité des IDs | users | 100% |
| Coordonnées dans CI | users | 99.8% |
| Cohérence temporelle | mobility | 99.5% |
| Vitesses réalistes | mobility | 99.2% |
| Distances cohérentes | migration | 99.7% |

### 3.8.2 Valeurs manquantes

| Dataset | Variable | % manquant |
|---------|----------|------------|
| users | Tous | 0% |
| poverty | data_mb | 3.2% |
| poverty | international_calls | 5.1% |
| migration | previous_locations | 8.5% |
| mobility | transport_mode | 2.8% |

### 3.8.3 Cohérence inter-datasets

| Vérification | Résultat |
|--------------|----------|
| users.user_id ⊆ poverty.user_id | ✅ 100% |
| migration.user_id ⊆ users.user_id | ✅ 100% |
| mobility.user_id ⊆ users.user_id | ✅ 100% |
| Coordonnées dans limites GADM | ✅ 99.8% |

---

## 3.9 Limitations et biais potentiels

### 3.9.1 Limitations des données synthétiques

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Pas de vraies traces CDR | Patterns simplifiés | Calibration sur études |
| Corrélations artificielles | Risque de surestimation | Validation croisée |
| Volume réduit | Précision limitée | Tests de sensibilité |

### 3.9.2 Biais de couverture

| Population | Représentation | Commentaire |
|------------|----------------|-------------|
| Possesseurs de mobile | ✅ Bonne | 98% de couverture |
| Multi-SIM | ⚠️ Partielle | 1 SIM = 1 utilisateur |
| Enfants < 15 ans | ❌ Faible | Peu de téléphones |
| Personnes âgées | ⚠️ Partielle | Adoption plus faible |
| Zones reculées | ⚠️ Partielle | Couverture réseau limitée |

### 3.9.3 Biais de génération

| Biais | Description | Traitement |
|-------|-------------|------------|
| Spatial | Sur-représentation d'Abidjan | Pondération |
| Temporel | Période de 30 jours | Extrapolation prudente |
| Comportemental | Simplification des patterns | Validation qualitative |

---

## 3.10 Synthèse

### Récapitulatif des datasets

| Dataset | Lignes | Colonnes | Clé | Période |
|---------|--------|----------|-----|---------|
| users | 10 000 | 15 | user_id | - |
| poverty | 50 000 | 18 | (user_id, month) | 5 mois |
| migration | ~500 | 15 | (user_id, timestamp) | 12 mois |
| mobility | ~17 000 | 18 | (user_id, timestamp) | 30 jours |

### Points clés

1. **Données synthétiques** calibrées sur les statistiques officielles (RGPH 2021, ENV 2018)
2. **4 datasets interconnectés** via l'identifiant utilisateur
3. **Indexation spatiale H3** pour l'anonymisation et l'agrégation
4. **Qualité contrôlée** avec >95% de complétude
5. **Limitations documentées** pour une interprétation prudente des résultats

---

# 4. Méthodologie d'estimation de la pauvreté

---

## 4.1 Standards et classifications

### 4.1.1 Normes de métadonnées

Les métadonnées des datasets suivent les standards suivants :

| Domaine | Standard | Description |
|---------|----------|-------------|
| **Général** | Dublin Core | Éléments de base |
| **Données** | Data Catalog Vocabulary (DCAT) | Profil de données |
| **Propriétaire** | ISO 19115 | Métadonnées géographiques |

### 4.1.2 Classification des données

Les données sont classées selon les dimensions suivantes :

| Dimension | Type | Niveaux |
|-----------|------|---------|
| **Temps** | Périodique | Mensuel |
| **Espace** | Géographique | Région, district |
| **Sujets** | Thématique | Démographie, économie, mobilité |

### 4.1.3 Conformité aux standards

| Standard | Application |
|----------|-------------|
| **UN-MPDMS v2.0** | Définitions migration, indicateurs |
| **SDMX** | Structure des métadonnées |
| **ISO 19115** | Métadonnées géographiques |
| **RGPD (principes)** | Protection des données |

---

## 4.2 Indicateurs de pauvreté

### 4.2.1 Fondements théoriques

L'estimation de la pauvreté à partir des données CDR repose sur l'hypothèse que les **comportements téléphoniques** sont corrélés au **statut socio-économique**.

**Études fondatrices** :
- Blumenstock et al. (2015) : Prédiction de la pauvreté au Rwanda
- Steele et al. (2017) : Cartographie de la pauvreté au Bangladesh
- Pokhriyal & Jacques (2017) : Estimation de la richesse en Sénégal

### 4.2.2 Variables prédictives

Les variables CDR utilisées comme proxies de richesse :

| Variable | Hypothèse | Corrélation attendue |
|----------|-----------|---------------------|
| `recharge_amount_fcfa` | Capacité financière | Positive |
| `call_duration_sec` | Ressources pour communication | Positive |
| `data_mb` | Accès à internet/smartphone | Positive |
| `unique_contacts` | Capital social | Positive |
| `mobility_radius_km` | Accès aux transports | Positive |
| `contact_diversity_score` | Réseau social étendu | Positive |
| `night_activity_ratio` | Emploi informel/précaire | Négative |
| `international_calls` | Diaspora, transferts | Positive |

### 4.2.3 Méthode 1 : Analyse en Composantes Principales (ACP)

#### Principe

L'ACP permet de **réduire la dimensionnalité** des variables CDR en extrayant les composantes principales qui expliquent le maximum de variance.

#### Formulation mathématique

Soit $X$ la matrice des données centrées-réduites ($n$ observations × $p$ variables) :

$$X_{standardisé} = \frac{X - \mu}{\sigma}$$

L'ACP décompose la matrice de covariance :

$$\Sigma = \frac{1}{n-1} X^T X = V \Lambda V^T$$

où :
- $V$ : matrice des vecteurs propres (composantes principales)
- $\Lambda$ : matrice diagonale des valeurs propres

#### Interprétation des résultats

- **Composantes principales** : Nouvelles variables non corrélées
- **Variance expliquée** : Proportion de la variance totale

### 4.2.4 Méthode 2 : Modèles de régression

#### Régression linéaire

Modèle simple pour estimer l'indice de richesse :

$$wealth\_index = \beta_0 + \beta_1 \times recharge\_amount\_fcfa + \beta_2 \times call\_duration\_sec + \epsilon$$

#### Régression logistique

Pour prédire la probabilité d'appartenance à un quintile de richesse :

$$logit(p) = \beta_0 + \beta_1 \times data\_mb + \beta_2 \times unique\_contacts + \epsilon$$

### 4.2.5 Validation des modèles

- **Jeu de données de test** : 20% des données
- **Métriques** : RMSE, R² pour la régression ; précision, rappel pour la classification

---

## 4.3 Estimation de l'indice de pauvreté multidimensionnelle (IPM)

### 4.3.1 Méthodologie IPM

L'IPM évalue la pauvreté sur plusieurs dimensions (santé, éducation, niveau de vie) :

$$IPM = \phi_{headcount} \times \phi_{intensité}$$

où :
- $\phi_{headcount}$ : Taux de pauvreté (proportion de la population pauvre)
- $\phi_{intensité}$ : Intensité de la pauvreté (écart moyen des pauvres par rapport au seuil de pauvreté)

### 4.3.2 Données nécessaires

- **Santé** : Accès aux soins, fréquence des maladies
- **Éducation** : Taux de scolarisation, niveau d'éducation
- **Niveau de vie** : Qualité du logement, accès à l'eau potable

### 4.3.3 Agrégation des données

- **Par utilisateur** : Agrégation des indicateurs de santé, éducation, niveau de vie
- **Par région** : Moyenne pondérée des indices des utilisateurs

### 4.3.4 Calcul de l'IPM

- **Seuils de pauvreté** : Déterminés par des études locales
- **Pondérations** : Basées sur l'importance relative des dimensions

---

## 4.4 Limites de la méthodologie

- **Données incomplètes** : Manque d'indicateurs directs de pauvreté
- **Hypothèses simplificatrices** : Corrélations supposées entre variables
- **Validité externe** : Résultats valables principalement pour la Côte d'Ivoire

---

**Document** : Description des données  
**Version** : 1.1  
**Date** : Janvier 2026  
**Projet** : CI-Mobility-Prototype  
**Standard** : UN-MPDMS v2.0
