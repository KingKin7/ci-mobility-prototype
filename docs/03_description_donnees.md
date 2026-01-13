# 3. Description des Données

## 3.1 Vue d'ensemble

### 3.1.1 Sources de données

Ce projet utilise deux types de sources :

| Type | Source | Usage |
|------|--------|-------|
| **Données synthétiques** | Générateur algorithmique | Développement et tests |
| **Données géographiques** | GADM v4.1 | Limites administratives |

### 3.1.2 Datasets générés

Le pipeline produit quatre datasets principaux :

| Dataset | Description | Volume type |
|---------|-------------|-------------|
| `users` | Profils des utilisateurs simulés | 10 000 enregistrements |
| `poverty` | Indicateurs comportementaux CDR | 50 000 enregistrements |
| `migration` | Événements de migration détectés | 500 enregistrements |
| `mobility` | Trajets quotidiens | 15 000 - 20 000 enregistrements |

### 3.1.3 Formats de fichiers

| Format | Extension | Usage |
|--------|-----------|-------|
| Parquet | `.parquet` | Stockage optimisé |
| CSV | `.csv` | Export et interopérabilité |
| GeoJSON | `.json` | Données géographiques |
| Excel | `.xlsx` | Rapports et statistiques |

## 3.2 Dataset : Users (Profils utilisateurs)

### 3.2.1 Description

Le dataset `users` contient les profils démographiques et de localisation des utilisateurs simulés. Chaque enregistrement représente un utilisateur unique de téléphonie mobile.

### 3.2.2 Dictionnaire des variables

| Variable | Type | Description | Exemple |
|----------|------|-------------|---------|
| `user_id` | string | Identifiant unique anonymisé | `USR_00001` |
| `age_group` | string | Tranche d'âge (5 catégories) | `25-34` |
| `gender` | string | Genre (M/F) | `F` |
| `phone_type` | string | Type de téléphone | `smartphone` |
| `locality` | string | Localité de résidence | `Abobo` |
| `region` | string | Région administrative | `Abidjan` |
| `district` | string | District | `Abidjan` |
| `urban_rural` | string | Type de zone | `urban` |
| `home_lat` | float | Latitude du domicile | `5.4321` |
| `home_lon` | float | Longitude du domicile | `-4.0123` |
| `home_h3` | string | Cellule H3 résolution 8 | `88754a6...` |
| `socio_economic_proxy` | float | Proxy socio-économique [0-1] | `0.65` |
| `activity_level` | string | Niveau d'activité mobile | `high` |
| `registration_date` | datetime | Date d'enregistrement SIM | `2024-03-15` |

### 3.2.3 Distributions attendues

**Répartition par genre :**
| Genre | Pourcentage |
|-------|-------------|
| Masculin | 51% |
| Féminin | 49% |

**Répartition par groupe d'âge :**
| Groupe | Pourcentage |
|--------|-------------|
| 15-24 | 25% |
| 25-34 | 30% |
| 35-44 | 22% |
| 45-54 | 14% |
| 55+ | 9% |

**Répartition urbain/rural :**
| Zone | Pourcentage |
|------|-------------|
| Urbain | 55% |
| Rural | 45% |

**Types de téléphone :**
| Type | Pourcentage |
|------|-------------|
| Smartphone | 45% |
| Feature phone | 40% |
| Basic phone | 15% |

## 3.3 Dataset : Poverty (Indicateurs de pauvreté)

### 3.3.1 Description

Le dataset `poverty` contient les indicateurs comportementaux extraits des CDR (Call Detail Records) simulés. Ces variables servent de proxy pour estimer le niveau de richesse.

### 3.3.2 Dictionnaire des variables

| Variable | Type | Unité | Description |
|----------|------|-------|-------------|
| `user_id` | string | - | Identifiant utilisateur |
| `period` | string | - | Période de mesure (YYYY-MM) |
| `region` | string | - | Région de résidence |
| `recharge_amount_fcfa` | float | FCFA | Montant total des recharges |
| `recharge_frequency_weekly` | float | /semaine | Fréquence de recharge |
| `call_duration_sec` | float | secondes | Durée totale des appels |
| `sms_count` | int | - | Nombre de SMS envoyés |
| `data_mb` | float | Mo | Consommation de données |
| `contact_diversity_score` | float | [0-1] | Diversité du réseau social |
| `nocturnal_activity_ratio` | float | [0-1] | Ratio d'activité nocturne |
| `weekend_activity_ratio` | float | [0-1] | Ratio d'activité weekend |
| `mobility_radius_km` | float | km | Rayon de mobilité moyen |
| `unique_locations_visited` | int | - | Nombre de lieux visités |
| `international_contacts` | int | - | Contacts internationaux |
| `handset_price_proxy` | float | [0-1] | Proxy prix du téléphone |

### 3.3.3 Indicateurs calculés (ajoutés par le pipeline)

| Variable | Type | Description | Méthode |
|----------|------|-------------|---------|
| `wealth_index` | float | Indice de richesse [-3, 3] | ACP |
| `wealth_quintile` | int | Quintile de richesse [1-5] | Percentiles |
| `mpi_score` | float | Score IPM [0-1] | Alkire-Foster |
| `is_mpi_poor` | bool | Pauvre multidimensionnel | Seuil k=0.33 |
| `deprivation_count` | int | Nombre de privations | Comptage |

### 3.3.4 Corrélations attendues avec la richesse

| Variable | Corrélation attendue | Justification |
|----------|---------------------|---------------|
| `recharge_amount_fcfa` | Positive forte | Capacité financière |
| `data_mb` | Positive forte | Accès aux services numériques |
| `contact_diversity_score` | Positive modérée | Capital social |
| `mobility_radius_km` | Positive modérée | Accès aux transports |
| `nocturnal_activity_ratio` | Variable | Dépend du contexte |

## 3.4 Dataset : Migration (Événements de migration)

### 3.4.1 Description

Le dataset `migration` contient les événements de migration interne détectés à partir des changements de localisation résidentielle des utilisateurs.

### 3.4.2 Dictionnaire des variables

| Variable | Type | Description | Exemple |
|----------|------|-------------|---------|
| `user_id` | string | Identifiant utilisateur | `USR_00123` |
| `timestamp` | datetime | Date de détection | `2025-06-15` |
| `origin_locality` | string | Localité d'origine | `Bouaké` |
| `origin_region` | string | Région d'origine | `Gbêkê` |
| `origin_lat` | float | Latitude origine | `7.6833` |
| `origin_lon` | float | Longitude origine | `-5.0167` |
| `current_locality` | string | Localité de destination | `Abidjan` |
| `current_region` | string | Région de destination | `Abidjan` |
| `current_lat` | float | Latitude destination | `5.3167` |
| `current_lon` | float | Longitude destination | `-4.0333` |
| `distance_km` | float | Distance parcourue | `356.2` |
| `residence_duration_days` | int | Durée au nouveau lieu | `45` |
| `movement_type` | string | Type de migration | `long_distance` |
| `is_return_migration` | bool | Migration de retour | `False` |
| `previous_locations` | list | Historique des lieux | `[...]` |

### 3.4.3 Types de migration

| Type | Critère | Description |
|------|---------|-------------|
| `long_distance` | > 200 km | Migration longue distance |
| `regional` | 50 - 200 km | Migration régionale |
| `local` | < 50 km | Migration locale |
| `return` | Retour origine | Migration de retour |
| `circular` | Répétée | Migration circulaire |
| `seasonal` | Saisonnière | Migration saisonnière |

### 3.4.4 Critères de détection UN-MPDMS

Pour qu'un mouvement soit classifié comme migration :

1. **Distance minimale** : > 50 km (paramétrable)
2. **Durée minimale** : > 30 jours au nouveau lieu
3. **Confiance** : Score de confiance > 0.7
4. **Changement de résidence** : Nouveau lieu identifié comme domicile

## 3.5 Dataset : Mobility (Trajets quotidiens)

### 3.5.1 Description

Le dataset `mobility` contient les trajets quotidiens des utilisateurs, reconstruits à partir des événements de localisation (connexions aux antennes).

### 3.5.2 Dictionnaire des variables

| Variable | Type | Unité | Description |
|----------|------|-------|-------------|
| `user_id` | string | - | Identifiant utilisateur |
| `trip_id` | string | - | Identifiant unique du trajet |
| `date` | date | - | Date du trajet |
| `start_time` | datetime | - | Heure de départ |
| `end_time` | datetime | - | Heure d'arrivée |
| `hour_of_day` | int | heure | Heure de départ [0-23] |
| `day_of_week` | int | - | Jour de la semaine [0-6] |
| `origin_h3` | string | - | Cellule H3 origine |
| `destination_h3` | string | - | Cellule H3 destination |
| `origin_locality` | string | - | Localité d'origine |
| `destination_locality` | string | - | Localité de destination |
| `distance_km` | float | km | Distance du trajet |
| `duration_min` | float | minutes | Durée du trajet |
| `speed_kmh` | float | km/h | Vitesse moyenne |
| `transport_mode` | string | - | Mode de transport inféré |
| `trip_purpose` | string | - | Motif du déplacement |
| `is_commute` | bool | - | Trajet domicile-travail |

### 3.5.3 Modes de transport inférés

| Mode | Critère vitesse | Part attendue |
|------|-----------------|---------------|
| `walking` | < 6 km/h | 25% |
| `bicycle` | 6 - 20 km/h | 5% |
| `gbaka` (minibus) | 10 - 30 km/h | 35% |
| `taxi` | 15 - 40 km/h | 15% |
| `personal_vehicle` | 20 - 80 km/h | 15% |
| `bus` | 10 - 35 km/h | 5% |

### 3.5.4 Motifs de déplacement

| Motif | Description | Part attendue |
|-------|-------------|---------------|
| `work` | Domicile → Travail | 35% |
| `education` | Vers établissement scolaire | 15% |
| `shopping` | Achats et marché | 20% |
| `leisure` | Loisirs et visites | 15% |
| `health` | Soins médicaux | 5% |
| `other` | Autres motifs | 10% |

## 3.6 Données géographiques

### 3.6.1 Limites administratives GADM

| Attribut | Valeur |
|----------|--------|
| **Source** | GADM v4.1 |
| **Fichier** | `gadm41_CIV_4.json` |
| **Format** | GeoJSON |
| **CRS** | WGS84 (EPSG:4326) |
| **Niveau** | 4 (sous-préfectures) |
| **Nombre d'unités** | 191 |

### 3.6.2 Indexation spatiale H3

Le projet utilise le système d'indexation **H3** d'Uber pour l'agrégation spatiale :

| Résolution | Aire moyenne | Usage |
|------------|--------------|-------|
| 5 | ~253 km² | Niveau régional |
| 6 | ~36 km² | Niveau département |
| 7 | ~5 km² | Niveau commune |
| **8** | **~0.74 km²** | **Niveau par défaut** |
| 9 | ~0.1 km² | Niveau fin |

### 3.6.3 Avantages de H3

1. **Uniformité** : Cellules hexagonales de taille quasi-égale
2. **Hiérarchie** : Emboîtement multi-résolution
3. **Efficacité** : Indexation rapide et requêtes spatiales optimisées
4. **Standard** : Utilisé par de nombreux acteurs du secteur

## 3.7 Qualité des données

### 3.7.1 Contrôles de qualité

| Contrôle | Description | Seuil |
|----------|-------------|-------|
| Complétude | % de valeurs non-nulles | > 95% |
| Unicité | % d'identifiants uniques | 100% |
| Cohérence | Valeurs dans plages attendues | 100% |
| Validité géographique | Coordonnées en CI | 100% |

### 3.7.2 Valeurs manquantes

| Dataset | Taux de complétion |
|---------|-------------------|
| `users` | 99.5% |
| `poverty` | 98.0% |
| `migration` | 97.0% |
| `mobility` | 96.0% |

### 3.7.3 Limitations connues

1. **Données synthétiques** : Patterns simplifiés par rapport à la réalité
2. **Biais de génération** : Distributions parfois trop régulières
3. **Corrélations artificielles** : Certaines relations peuvent être exagérées
4. **Absence de bruit** : Données plus propres que des données réelles

---

*Dernière mise à jour : Janvier 2026*  
*Standard : UN-MPDMS v2.0*