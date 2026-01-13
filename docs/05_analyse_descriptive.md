# 5. Analyse Descriptive

## 5.1 Vue d'ensemble des données

### 5.1.1 Résumé des datasets

| Dataset | Enregistrements | Variables | Taille |
|---------|-----------------|-----------|--------|
| `users` | 10 000 | 14 | 2.1 Mo |
| `poverty` | 50 000 | 15 | 8.5 Mo |
| `migration` | 500 | 15 | 0.2 Mo |
| `mobility` | 16 852 | 16 | 3.8 Mo |

### 5.1.2 Période couverte

- **Début** : 1er janvier 2025
- **Fin** : 31 décembre 2025
- **Durée** : 12 mois
- **Granularité** : Journalière

## 5.2 Profils des utilisateurs

### 5.2.1 Distribution géographique

**Top 10 des localités par nombre d'utilisateurs :**

| Rang | Localité | Utilisateurs | Part (%) |
|------|----------|--------------|----------|
| 1 | Abidjan | 2 847 | 28.5% |
| 2 | Bouaké | 612 | 6.1% |
| 3 | Korhogo | 398 | 4.0% |
| 4 | Daloa | 367 | 3.7% |
| 5 | San-Pédro | 312 | 3.1% |
| 6 | Yamoussoukro | 298 | 3.0% |
| 7 | Man | 256 | 2.6% |
| 8 | Gagnoa | 234 | 2.3% |
| 9 | Divo | 198 | 2.0% |
| 10 | Abengourou | 187 | 1.9% |

### 5.2.2 Caractéristiques démographiques

**Distribution par genre :**

| Genre | Effectif | Pourcentage |
|-------|----------|-------------|
| Masculin | 5 123 | 51.2% |
| Féminin | 4 877 | 48.8% |

**Distribution par groupe d'âge :**

| Groupe d'âge | Effectif | Pourcentage |
|--------------|----------|-------------|
| 15-24 | 2 498 | 25.0% |
| 25-34 | 3 012 | 30.1% |
| 35-44 | 2 187 | 21.9% |
| 45-54 | 1 423 | 14.2% |
| 55+ | 880 | 8.8% |

**Distribution par type de téléphone :**

| Type | Effectif | Pourcentage |
|------|----------|-------------|
| Smartphone | 4 512 | 45.1% |
| Feature phone | 3 987 | 39.9% |
| Basic phone | 1 501 | 15.0% |

### 5.2.3 Répartition urbain/rural

| Zone | Effectif | Pourcentage |
|------|----------|-------------|
| Urbain | 5 487 | 54.9% |
| Rural | 4 513 | 45.1% |

## 5.3 Indicateurs de pauvreté

### 5.3.1 Statistiques descriptives des variables CDR

| Variable | Moyenne | Médiane | Écart-type | Min | Max |
|----------|---------|---------|------------|-----|-----|
| Recharge (FCFA) | 12 450 | 8 500 | 15 230 | 500 | 125 000 |
| Appels (sec) | 3 245 | 2 100 | 4 120 | 0 | 45 000 |
| Data (Mo) | 856 | 320 | 1 450 | 0 | 15 000 |
| Contacts uniques | 45 | 32 | 38 | 5 | 350 |
| Mobilité (km) | 12.3 | 8.5 | 15.7 | 0.5 | 125 |

### 5.3.2 Indice de richesse

**Distribution de l'indice de richesse :**

| Statistique | Valeur |
|-------------|--------|
| Moyenne | 0.00 |
| Médiane | -0.12 |
| Écart-type | 1.00 |
| Skewness | 0.85 |
| Kurtosis | 3.21 |
| Min | -2.87 |
| Max | 3.45 |

**Variance expliquée par l'ACP :**

| Composante | Variance (%) | Cumul (%) |
|------------|--------------|-----------|
| PC1 | 57.7% | 57.7% |
| PC2 | 18.3% | 76.0% |
| PC3 | 9.8% | 85.8% |
| PC4 | 6.2% | 92.0% |
| PC5 | 4.5% | 96.5% |

**Loadings de PC1 (Indice de richesse) :**

| Variable | Loading | Interprétation |
|----------|---------|----------------|
| recharge_amount_fcfa | 0.52 | Fort positif |
| data_mb | 0.48 | Fort positif |
| call_duration_sec | 0.42 | Modéré positif |
| contact_diversity | 0.35 | Modéré positif |
| mobility_radius_km | 0.31 | Modéré positif |
| recharge_frequency | 0.25 | Faible positif |

### 5.3.3 Distribution par quintile

| Quintile | Effectif | Part (%) | Indice moyen | Recharge moyenne |
|----------|----------|----------|--------------|------------------|
| Q1 (Plus pauvre) | 10 000 | 20% | -1.45 | 3 200 FCFA |
| Q2 | 10 000 | 20% | -0.58 | 6 800 FCFA |
| Q3 | 10 000 | 20% | -0.02 | 10 500 FCFA |
| Q4 | 10 000 | 20% | 0.54 | 15 200 FCFA |
| Q5 (Plus riche) | 10 000 | 20% | 1.51 | 26 500 FCFA |

### 5.3.4 Indice de Pauvreté Multidimensionnelle

| Indicateur | Valeur |
|------------|--------|
| Incidence (H) | 42.3% |
| Intensité (A) | 48.7% |
| **IPM (H × A)** | **0.206** |

**Distribution des privations :**

| Nombre de privations | Effectif | Part (%) |
|---------------------|----------|----------|
| 0 | 15 234 | 30.5% |
| 1 | 13 567 | 27.1% |
| 2 | 11 245 | 22.5% |
| 3 | 9 954 | 19.9% |

### 5.3.5 Variations spatiales

**Taux de pauvreté (Q1+Q2) par région :**

| Région | Taux pauvreté | Indice moyen |
|--------|---------------|--------------|
| Savanes (Nord) | 58.2% | -0.67 |
| Woroba | 52.1% | -0.52 |
| Zanzan | 49.8% | -0.45 |
| Denguélé | 48.5% | -0.41 |
| Vallée du Bandama | 45.2% | -0.32 |
| ... | ... | ... |
| Lagunes | 28.4% | 0.35 |
| Comoé | 26.7% | 0.42 |
| **Abidjan** | **22.1%** | **0.58** |

## 5.4 Événements de migration

### 5.4.1 Volume et caractéristiques

| Indicateur | Valeur |
|------------|--------|
| Nombre total de migrations | 500 |
| Taux de migration (annuel) | 5.0% |
| Distance moyenne | 142.5 km |
| Distance médiane | 98.3 km |
| Durée moyenne de résidence | 67 jours |

### 5.4.2 Types de migration

| Type | Effectif | Part (%) | Distance moyenne |
|------|----------|----------|------------------|
| Regional | 245 | 49.0% | 87.5 km |
| Long distance | 156 | 31.2% | 285.3 km |
| Local | 52 | 10.4% | 32.1 km |
| Return | 35 | 7.0% | 156.8 km |
| Circular | 12 | 2.4% | 124.2 km |

### 5.4.3 Principaux corridors migratoires

**Top 10 des flux origine-destination :**

| Rang | Origine | Destination | Flux | Distance |
|------|---------|-------------|------|----------|
| 1 | Bouaké | Abidjan | 45 | 356 km |
| 2 | Korhogo | Abidjan | 38 | 592 km |
| 3 | Man | Abidjan | 32 | 579 km |
| 4 | Daloa | Abidjan | 28 | 383 km |
| 5 | San-Pédro | Abidjan | 24 | 348 km |
| 6 | Abidjan | Bouaké | 21 | 356 km |
| 7 | Gagnoa | Abidjan | 19 | 275 km |
| 8 | Yamoussoukro | Abidjan | 17 | 240 km |
| 9 | Bondoukou | Abidjan | 15 | 425 km |
| 10 | Abidjan | San-Pédro | 14 | 348 km |

### 5.4.4 Soldes migratoires par région

| Région | Immigration | Émigration | Solde | Efficacité |
|--------|-------------|------------|-------|------------|
| Abidjan | 312 | 87 | +225 | +0.56 |
| Lagunes | 45 | 28 | +17 | +0.23 |
| San-Pédro | 38 | 42 | -4 | -0.05 |
| Bouaké | 35 | 67 | -32 | -0.31 |
| Korhogo | 28 | 52 | -24 | -0.30 |
| Man | 22 | 48 | -26 | -0.37 |

### 5.4.5 Saisonnalité

**Distribution mensuelle des migrations :**

| Mois | Migrations | Part (%) | Observation |
|------|------------|----------|-------------|
| Janvier | 52 | 10.4% | Post-fêtes, retours |
| Février | 48 | 9.6% | Stable |
| Mars | 45 | 9.0% | Fin saison sèche |
| Avril | 38 | 7.6% | Début pluies |
| Mai | 35 | 7.0% | Saison agricole |
| Juin | 32 | 6.4% | Minimum annuel |
| Juillet | 42 | 8.4% | Vacances scolaires |
| Août | 48 | 9.6% | Pic vacances |
| Septembre | 38 | 7.6% | Rentrée |
| Octobre | 42 | 8.4% | Stable |
| Novembre | 35 | 7.0% | Pré-fêtes |
| Décembre | 45 | 9.0% | Fêtes de fin d'année |

**Analyse de la saisonnalité :**

- **Pics migratoires** : Janvier (10.4%), Août (9.6%), Février (9.6%)
- **Creux migratoires** : Juin (6.4%), Mai (7.0%), Novembre (7.0%)
- **Amplitude saisonnière** : 4.0 points de pourcentage
- **Coefficient de variation** : 15.2%

**Facteurs explicatifs de la saisonnalité :**

1. **Calendrier agricole** : Réduction des migrations pendant les périodes de semis (mai-juin) et de récolte (octobre-novembre)
2. **Calendrier scolaire** : Augmentation pendant les vacances (juillet-août)
3. **Fêtes traditionnelles** : Retours au village pour les célébrations (décembre-janvier)
4. **Conditions climatiques** : Réduction pendant la grande saison des pluies (mai-juillet)

## 5.5 Mobilité quotidienne

### 5.5.1 Volume et caractéristiques générales

| Indicateur | Valeur |
|------------|--------|
| Nombre total de trajets | 16 852 |
| Trajets moyens par utilisateur | 16.9 |
| Distance totale parcourue | 142 567 km |
| Durée totale | 48 523 heures |

### 5.5.2 Statistiques des trajets

| Métrique | Moyenne | Médiane | Écart-type | P10 | P90 |
|----------|---------|---------|------------|-----|-----|
| Distance (km) | 8.46 | 5.23 | 12.34 | 1.2 | 18.5 |
| Durée (min) | 28.5 | 18.0 | 32.1 | 5.0 | 65.0 |
| Vitesse (km/h) | 17.8 | 15.2 | 12.4 | 4.5 | 35.0 |

### 5.5.3 Répartition modale

| Mode de transport | Trajets | Part (%) | Distance moy. | Durée moy. |
|-------------------|---------|----------|---------------|------------|
| Marche | 5 234 | 31.1% | 1.8 km | 22 min |
| Gbaka (minibus) | 4 123 | 24.5% | 8.5 km | 35 min |
| Woro-woro (taxi collectif) | 2 987 | 17.7% | 5.2 km | 18 min |
| Moto | 2 156 | 12.8% | 6.8 km | 15 min |
| Taxi | 1 245 | 7.4% | 12.3 km | 25 min |
| Véhicule personnel | 892 | 5.3% | 18.5 km | 28 min |
| Bus SOTRA | 215 | 1.3% | 15.2 km | 45 min |

### 5.5.4 Distribution temporelle

**Distribution horaire des départs :**

| Période | Heures | Trajets | Part (%) |
|---------|--------|---------|----------|
| Nuit | 00h-06h | 512 | 3.0% |
| Pointe matin | 06h-09h | 4 523 | 26.8% |
| Journée | 09h-16h | 5 867 | 34.8% |
| Pointe soir | 16h-20h | 4 234 | 25.1% |
| Soirée | 20h-24h | 1 716 | 10.2% |

**Heures de pointe identifiées :**

| Indicateur | Matin | Soir |
|------------|-------|------|
| Heure pic | 07h30 | 17h30 |
| Volume pic horaire | 1 523 | 1 412 |
| Durée pointe | 2h30 | 3h00 |
| Indice de congestion | 1.85 | 2.12 |

### 5.5.5 Motifs de déplacement

| Motif | Trajets | Part (%) | Distance moy. | Heure moy. |
|-------|---------|----------|---------------|------------|
| Travail | 5 678 | 33.7% | 10.2 km | 07h15 |
| Commerce/Marché | 3 456 | 20.5% | 6.8 km | 09h30 |
| Domicile (retour) | 4 123 | 24.5% | 9.5 km | 18h00 |
| Loisirs | 1 567 | 9.3% | 5.2 km | 15h00 |
| Santé | 892 | 5.3% | 8.5 km | 10h00 |
| Éducation | 756 | 4.5% | 4.2 km | 07h00 |
| Autre | 380 | 2.3% | 7.8 km | 12h00 |

### 5.5.6 Analyse spatiale de la mobilité

**Rayon de mobilité par zone :**

| Zone | Rayon moyen (km) | Rayon médian (km) | Trajets/jour |
|------|------------------|-------------------|--------------|
| Abidjan Centre | 5.2 | 3.8 | 2.8 |
| Abidjan Périphérie | 12.4 | 8.5 | 2.1 |
| Villes secondaires | 8.7 | 6.2 | 1.8 |
| Zones rurales | 15.3 | 10.1 | 1.2 |

**Matrice de flux simplifiée (Abidjan) :**

| Origine \ Destination | Plateau | Cocody | Yopougon | Abobo | Marcory |
|-----------------------|---------|--------|----------|-------|---------|
| Plateau | - | 245 | 312 | 189 | 278 |
| Cocody | 267 | - | 156 | 134 | 198 |
| Yopougon | 345 | 178 | - | 423 | 156 |
| Abobo | 198 | 145 | 456 | - | 112 |
| Marcory | 289 | 212 | 167 | 98 | - |

### 5.5.7 Indicateurs de congestion

| Indicateur | Valeur | Interprétation |
|------------|--------|----------------|
| Indice de congestion moyen | 1.45 | Modéré |
| Temps perdu moyen (min/trajet) | 8.5 | Significatif |
| Vitesse heure de pointe (km/h) | 12.3 | Lent |
| Vitesse heure creuse (km/h) | 25.6 | Normal |
| Ratio pointe/creuse | 2.08 | Forte variation |

## 5.6 Corrélations et relations entre variables

### 5.6.1 Matrice de corrélation (variables clés)

| Variable | Recharge | Data | Mobilité | Contacts | Appels |
|----------|----------|------|----------|----------|--------|
| Recharge | 1.00 | 0.72 | 0.45 | 0.58 | 0.65 |
| Data | 0.72 | 1.00 | 0.38 | 0.52 | 0.48 |
| Mobilité | 0.45 | 0.38 | 1.00 | 0.42 | 0.35 |
| Contacts | 0.58 | 0.52 | 0.42 | 1.00 | 0.68 |
| Appels | 0.65 | 0.48 | 0.35 | 0.68 | 1.00 |

### 5.6.2 Relations pauvreté-mobilité

| Quintile | Mobilité moy. (km) | Trajets/jour | Mode dominant |
|----------|-------------------|--------------|---------------|
| Q1 | 6.2 | 1.2 | Marche (65%) |
| Q2 | 8.5 | 1.5 | Marche (48%) |
| Q3 | 10.8 | 1.8 | Gbaka (42%) |
| Q4 | 14.2 | 2.2 | Gbaka (38%) |
| Q5 | 18.5 | 2.8 | Taxi/VP (45%) |

### 5.6.3 Relations pauvreté-migration

| Quintile | Taux migration | Distance moy. | Type dominant |
|----------|----------------|---------------|---------------|
| Q1 | 3.2% | 85 km | Local (52%) |
| Q2 | 4.5% | 112 km | Regional (48%) |
| Q3 | 5.2% | 145 km | Regional (51%) |
| Q4 | 5.8% | 178 km | Long distance (42%) |
| Q5 | 6.3% | 215 km | Long distance (55%) |

## 5.7 Qualité des données

### 5.7.1 Complétude

| Dataset | Variables complètes | Taux complétude | Variables avec NA |
|---------|---------------------|-----------------|-------------------|
| users | 14/14 | 100% | 0 |
| poverty | 14/15 | 93.3% | 1 (phone_type) |
| migration | 15/15 | 100% | 0 |
| mobility | 15/16 | 93.8% | 1 (congestion_level) |

### 5.7.2 Cohérence

| Vérification | Résultat | Statut |
|--------------|----------|--------|
| IDs utilisateurs uniques | 10 000 | ✅ |
| Dates dans la période | 100% | ✅ |
| Coordonnées en Côte d'Ivoire | 99.8% | ✅ |
| Distances cohérentes | 99.5% | ✅ |
| Vitesses réalistes (<150 km/h) | 99.2% | ✅ |

### 5.7.3 Représentativité

| Dimension | Données | RGPH 2021 | Écart |
|-----------|---------|-----------|-------|
| % Urbain | 54.9% | 52.7% | +2.2 pp |
| % Femmes | 48.8% | 49.2% | -0.4 pp |
| % 15-34 ans | 55.1% | 53.8% | +1.3 pp |
| % Abidjan | 28.5% | 25.3% | +3.2 pp |

---

## 5.8 Synthèse de l'analyse descriptive

### Points clés

1. **Population étudiée** : 10 000 utilisateurs représentatifs de la population ivoirienne avec une légère surreprésentation urbaine

2. **Pauvreté** : 
   - 40% de la population dans les quintiles les plus pauvres (Q1-Q2)
   - Fort gradient Nord-Sud avec les régions du Nord plus défavorisées
   - IPM de 0.206, comparable aux estimations nationales

3. **Migration** :
   - 5% de taux de migration annuel
   - Abidjan comme principal pôle d'attraction (+225 solde net)
   - Saisonnalité marquée liée aux calendriers agricole et scolaire

4. **Mobilité** :
   - 16.9 trajets par utilisateur sur la période
   - Prédominance de la marche (31%) et des transports collectifs informels (42%)
   - Heures de pointe bien identifiées (07h-09h et 17h-20h)

5. **Qualité des données** :
   - Complétude > 93% pour tous les datasets
   - Cohérence validée sur les principaux indicateurs
   - Représentativité acceptable avec écarts < 5 pp vs RGPH

---

**Document** : Analyse Descriptive  
**Version** : 1.0  
**Date** : Janvier 2026  
**Projet** : CI-Mobility-Prototype  
**Standard** : UN-MPDMS v2.0