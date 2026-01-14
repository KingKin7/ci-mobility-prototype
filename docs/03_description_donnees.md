# 3. Description des Données

## 3.1 Vue d'ensemble

### 3.1.1 Nature des données

Ce projet utilise des **données synthétiques** générées pour simuler des Call Detail Records (CDR) de téléphonie mobile. Ces données sont calibrées sur les statistiques officielles de la Côte d'Ivoire.

> ⚠️ **Important** : Les données sont entièrement synthétiques et ne proviennent pas de vrais utilisateurs. Elles sont conçues pour démontrer les méthodes analytiques applicables aux vraies données CDR.

### 3.1.2 Datasets générés

| Dataset | Description | Enregistrements | Colonnes |
|---------|-------------|-----------------|----------|
| `users` | Profils des utilisateurs | 10 000 | 15 |
| `poverty` | Indicateurs de pauvreté | 50 000 | 12 |
| `migration` | Événements de migration | 500 | 15 |
| `mobility` | Trajets quotidiens | ~17 000 | 18 |

### 3.1.3 Période de référence

| Paramètre | Valeur |
|-----------|--------|
| Période de génération | Janvier 2026 |
| Période simulée | 90 jours (3 mois) |
| Fréquence des observations | Variable selon le dataset |

---

## 3.2 Dataset : Utilisateurs (`users`)

### 3.2.1 Description

Le dataset `users` contient les profils des 10 000 utilisateurs simulés. Chaque utilisateur représente un abonné mobile unique avec ses caractéristiques socio-démographiques et sa localisation de résidence.

### 3.2.2 Dictionnaire des variables

| Variable | Type | Description | Exemple |
|----------|------|-------------|---------|
| `user_id` | string | Identifiant unique anonymisé | "USR_00001" |
| `age` | integer | Âge en années | 32 |
| `age_group` | string | Tranche d'âge | "25-34" |
| `gender` | string | Genre (M/F) | "M" |
| `phone_type` | string | Type de téléphone | "smartphone" |
| `locality` | string | Localité de résidence | "Abobo" |
| `region` | string | Région administrative | "Abidjan" |
| `district` | string | District | "Abidjan" |
| `urban_rural` | string | Zone urbaine/rurale | "urban" |
| `home_lat` | float | Latitude du domicile | 5.4167 |
| `home_lon` | float | Longitude du domicile | -4.0167 |
| `home_h3` | string | Cellule H3 du domicile | "872a1072fffffff" |
| `socio_economic_score` | float | Score socio-économique [0-1] | 0.65 |
| `activity_level` | string | Niveau d'activité mobile | "high" |
| `registration_date` | datetime | Date d'inscription | "2024-03-15" |

### 3.2.3 Distributions attendues

**Répartition par genre** :
- Hommes : 51.2%
- Femmes : 48.8%

**Répartition par zone** :
- Urbain : 54.9%
- Rural : 45.1%

**Répartition par type de téléphone** :
- Smartphone : 45%
- Feature phone : 55%

### 3.2.4 Validation

| Règle | Critère | Statut |
|-------|---------|--------|
| Unicité | `user_id` unique | ✅ |
| Complétude | Pas de valeurs nulles sur colonnes clés | ✅ |
| Cohérence géographique | Coordonnées dans les limites de la CI | ✅ |
| Cohérence âge | 15 ≤ age ≤ 85 | ✅ |

---

## 3.3 Dataset : Pauvreté (`poverty`)

### 3.3.1 Description

Le dataset `poverty` contient les indicateurs de comportement mobile associés à la pauvreté. Chaque utilisateur a 5 observations (mensuelles) permettant d'analyser la temporalité.

### 3.3.2 Dictionnaire des variables

| Variable | Type | Description | Unité |
|----------|------|-------------|-------|
| `user_id` | string | Identifiant utilisateur | - |
| `period` | string | Période d'observation | "2026-01" |
| `region` | string | Région de résidence | - |
| `recharge_amount_fcfa` | float | Montant rechargé | FCFA |
| `recharge_frequency_weekly` | float | Fréquence de recharge | /semaine |
| `call_duration_sec` | float | Durée totale des appels | secondes |
| `sms_count` | integer | Nombre de SMS envoyés | - |
| `data_mb` | float | Consommation de données | Mo |
| `contact_diversity_score` | float | Diversité des contacts [0-1] | - |
| `mobility_radius_km` | float | Rayon de mobilité | km |
| `night_activity_ratio` | float | Ratio activité nocturne [0-1] | - |
| `international_calls_ratio` | float | Ratio appels internationaux [0-1] | - |

### 3.3.3 Statistiques descriptives

| Variable | Moyenne | Médiane | Écart-type | Min | Max |
|----------|---------|---------|------------|-----|-----|
| recharge_amount_fcfa | 8 500 | 5 000 | 12 000 | 100 | 150 000 |
| call_duration_sec | 1 800 | 1 200 | 2 500 | 0 | 25 000 |
| data_mb | 450 | 200 | 800 | 0 | 10 000 |
| mobility_radius_km | 15.2 | 8.5 | 20.3 | 0.5 | 150 |
| contact_diversity_score | 0.45 | 0.42 | 0.22 | 0.05 | 0.98 |

### 3.3.4 Corrélations avec la pauvreté

Les recherches montrent que ces indicateurs sont corrélés au niveau de richesse :

| Indicateur | Corrélation attendue | Référence |
|------------|---------------------|-----------|
| Montant recharge | Positive forte (+0.6) | Blumenstock et al., 2015 |
| Diversité contacts | Positive modérée (+0.4) | Eagle et al., 2010 |
| Rayon de mobilité | Positive modérée (+0.3) | Pappalardo et al., 2015 |
| Consommation data | Positive forte (+0.5) | Steele et al., 2017 |

---

## 3.4 Dataset : Migration (`migration`)

### 3.4.1 Description

Le dataset `migration` contient les événements de migration détectés, définis comme un changement de résidence habituelle de plus de 50 km pendant plus de 30 jours (standard UN-MPDMS).

### 3.4.2 Dictionnaire des variables

| Variable | Type | Description | Exemple |
|----------|------|-------------|---------|
| `user_id` | string | Identifiant utilisateur | "USR_00123" |
| `timestamp` | datetime | Date de détection | "2026-01-15" |
| `origin_locality` | string | Localité d'origine | "Bouaké" |
| `origin_region` | string | Région d'origine | "Vallée du Bandama" |
| `current_locality` | string | Localité de destination | "Abidjan" |
| `current_region` | string | Région de destination | "Abidjan" |
| `origin_lat` | float | Latitude origine | 7.6833 |
| `origin_lon` | float | Longitude origine | -5.0167 |
| `current_lat` | float | Latitude destination | 5.3167 |
| `current_lon` | float | Longitude destination | -4.0167 |
| `distance_km` | float | Distance de migration | 325.4 |
| `residence_duration_days` | integer | Durée à destination | 45 |
| `movement_type` | string | Type de migration | "migration_travail" |
| `is_return_migration` | boolean | Migration de retour | False |
| `previous_locations` | list | Historique des lieux | [...] |

### 3.4.3 Types de migration

| Type | Description | Proportion |
|------|-------------|------------|
| `migration_travail` | Migration pour emploi | 35% |
| `agriculture_saisonniere` | Travail agricole saisonnier | 25% |
| `migration_etudes` | Migration pour études | 15% |
| `relocalisation_permanente` | Déménagement définitif | 15% |
| `migration_circulaire` | Allers-retours réguliers | 10% |

### 3.4.4 Principaux corridors migratoires

| Origine | Destination | Flux (%) |
|---------|-------------|----------|
| Vallée du Bandama | Abidjan | 18% |
| Savanes | Abidjan | 12% |
| Woroba | Bas-Sassandra | 8% |
| Gôh-Djiboua | Abidjan | 7% |
| Zanzan | Lagunes | 5% |

---

## 3.5 Dataset : Mobilité (`mobility`)

### 3.5.1 Description

Le dataset `mobility` contient les trajets quotidiens détectés à partir des changements de position des utilisateurs. Chaque enregistrement représente un déplacement entre deux points.

### 3.5.2 Dictionnaire des variables

| Variable | Type | Description | Unité |
|----------|------|-------------|-------|
| `trip_id` | string | Identifiant du trajet | - |
| `user_id` | string | Identifiant utilisateur | - |
| `date` | date | Date du trajet | - |
| `start_time` | time | Heure de départ | HH:MM |
| `end_time` | time | Heure d'arrivée | HH:MM |
| `hour_of_day` | integer | Heure de la journée | 0-23 |
| `day_of_week` | integer | Jour de la semaine | 0-6 |
| `origin_lat` | float | Latitude départ | degrés |
| `origin_lon` | float | Longitude départ | degrés |
| `destination_lat` | float | Latitude arrivée | degrés |
| `destination_lon` | float | Longitude arrivée | degrés |
| `origin_h3` | string | Cellule H3 départ | - |
| `destination_h3` | string | Cellule H3 arrivée | - |
| `distance_km` | float | Distance parcourue | km |
| `duration_min` | float | Durée du trajet | minutes |
| `speed_kmh` | float | Vitesse moyenne | km/h |
| `transport_mode` | string | Mode de transport | - |
| `trip_purpose` | string | Motif du déplacement | - |

### 3.5.3 Modes de transport

| Mode | Description | Proportion | Vitesse moy. |
|------|-------------|------------|--------------|
| `marche_a_pied` | À pied | 25% | 5 km/h |
| `moto` | Deux-roues | 20% | 25 km/h |
| `taxi` | Taxi (woro-woro, taxi-compteur) | 18% | 20 km/h |
| `bus` | Transport collectif (gbaka, bus) | 22% | 15 km/h |
| `voiture_personnelle` | Véhicule personnel | 15% | 30 km/h |

### 3.5.4 Motifs de déplacement

| Motif | Description | Proportion |
|-------|-------------|------------|
| `domicile_travail` | Aller au travail | 35% |
| `travail_domicile` | Retour du travail | 30% |
| `courses` | Achats, marché | 15% |
| `loisirs` | Visites, loisirs | 12% |
| `sante` | Consultations médicales | 5% |
| `autre` | Autres motifs | 3% |

### 3.5.5 Distribution temporelle

**Heures de pointe** :
- Matin : 07h00 - 09h00 (pic à 08h00)
- Soir : 17h00 - 20h00 (pic à 18h00)

**Jours de la semaine** :
- Lundi-Vendredi : ~16% chacun
- Samedi : 12%
- Dimanche : 8%

---

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