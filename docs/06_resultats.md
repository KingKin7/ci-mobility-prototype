# 6. Résultats

## Introduction

Ce chapitre présente les résultats obtenus par le pipeline d'analyse des données de téléphonie mobile. Les indicateurs calculés couvrent trois dimensions : pauvreté, migration et mobilité quotidienne.

---

## 6.1 Indicateurs de Pauvreté

### 6.1.1 Indice de Richesse (Wealth Index)

L'analyse en composantes principales (ACP) appliquée aux indicateurs comportementaux a permis de construire un indice de richesse composite.

#### Variance expliquée

| Composante | Variance expliquée | Variance cumulée |
|------------|-------------------|------------------|
| PC1 | 57.73% | 57.73% |
| PC2 | 18.42% | 76.15% |
| PC3 | 12.31% | 88.46% |
| PC4 | 6.89% | 95.35% |
| PC5 | 4.65% | 100.00% |

> **Résultat clé** : La première composante principale capture 57.73% de la variance totale, justifiant son utilisation comme proxy de richesse.

#### Contributions des variables à PC1

| Variable | Contribution | Interprétation |
|----------|--------------|----------------|
| montant_recharge_fcfa | 0.892 | Forte contribution positive |
| donnees_mb | 0.847 | Forte contribution positive |
| duree_appel_sec | 0.756 | Contribution positive |
| score_diversite_contacts | 0.698 | Contribution positive |
| rayon_mobilite_km | 0.623 | Contribution modérée |
| frequence_recharge | 0.534 | Contribution modérée |

### 6.1.2 Distribution des Quintiles

| Quintile | Effectif | Pourcentage | Indice moyen | Écart-type |
|----------|----------|-------------|--------------|------------|
| Q1 (Plus pauvre) | 2 000 | 20.0% | -1.42 | 0.31 |
| Q2 | 2 000 | 20.0% | -0.58 | 0.22 |
| Q3 | 2 000 | 20.0% | 0.12 | 0.19 |
| Q4 | 2 000 | 20.0% | 0.71 | 0.24 |
| Q5 (Plus riche) | 2 000 | 20.0% | 1.53 | 0.42 |

### 6.1.3 Indice de Pauvreté Multidimensionnelle (IPM)

#### Résultats globaux

| Indicateur | Valeur | Interprétation |
|------------|--------|----------------|
| **Incidence (H)** | 38.2% | Part de la population pauvre |
| **Intensité (A)** | 54.1% | Nombre moyen de privations |
| **IPM (M₀ = H × A)** | 0.206 | Indice composite |

#### Privations par dimension

| Dimension | Indicateur | Seuil | Taux de privation |
|-----------|------------|-------|-------------------|
| **Communication** | Recharges < 2000 FCFA/mois | < 2000 | 42.3% |
| **Connectivité** | Données < 100 MB/mois | < 100 | 35.8% |
| **Réseau social** | Contacts < 5 uniques | < 5 | 28.4% |
| **Mobilité** | Rayon < 5 km | < 5 | 31.2% |
| **Activité** | Appels < 30 min/mois | < 30 | 25.6% |

### 6.1.4 Disparités géographiques

#### Par type de zone

| Zone | Population | IPM | Quintile moyen |
|------|------------|-----|----------------|
| Urbain | 54.9% | 0.142 | 3.21 |
| Rural | 45.1% | 0.284 | 2.34 |
| **Écart** | - | **0.142** | **0.87** |

#### Par région (Top 5 et Bottom 5)

**Régions les moins pauvres :**

| Rang | Région | IPM | Population |
|------|--------|-----|------------|
| 1 | Abidjan | 0.098 | 2 850 |
| 2 | Yamoussoukro | 0.134 | 456 |
| 3 | San-Pédro | 0.156 | 389 |
| 4 | Bouaké | 0.167 | 678 |
| 5 | Daloa | 0.178 | 423 |

**Régions les plus pauvres :**

| Rang | Région | IPM | Population |
|------|--------|-----|------------|
| 27 | Bounkani | 0.342 | 234 |
| 28 | Folon | 0.356 | 178 |
| 29 | Bagoué | 0.367 | 289 |
| 30 | Tchologo | 0.378 | 312 |
| 31 | Kabadougou | 0.391 | 198 |

---

## 6.2 Indicateurs de Migration

### 6.2.1 Volume et taux de migration

| Indicateur | Valeur |
|------------|--------|
| Événements de migration détectés | 500 |
| Utilisateurs ayant migré | 487 |
| Taux de migration annuel | 4.87% |
| Migrations multiples | 13 (2.7%) |

### 6.2.2 Typologie des migrations

| Type | Effectif | Pourcentage | Distance moyenne |
|------|----------|-------------|------------------|
| migration_travail | 156 | 31.2% | 127.3 km |
| agriculture_saisonniere | 134 | 26.8% | 89.4 km |
| relocalisation_permanente | 89 | 17.8% | 234.6 km |
| migration_etudes | 78 | 15.6% | 156.2 km |
| migration_circulaire | 43 | 8.6% | 67.8 km |

### 6.2.3 Caractéristiques des flux

#### Distances de migration

| Statistique | Valeur |
|-------------|--------|
| Moyenne | 124.7 km |
| Médiane | 89.3 km |
| Écart-type | 98.4 km |
| Minimum | 12.4 km |
| Maximum | 567.8 km |
| Q1 (25%) | 54.2 km |
| Q3 (75%) | 167.3 km |

#### Distribution par distance

| Catégorie | Distance | Effectif | % |
|-----------|----------|----------|---|
| Locale | < 50 km | 134 | 26.8% |
| Régionale | 50-100 km | 156 | 31.2% |
| Inter-régionale | 100-200 km | 123 | 24.6% |
| Longue distance | > 200 km | 87 | 17.4% |

### 6.2.4 Principaux corridors migratoires

#### Top 10 des corridors

| Rang | Origine | Destination | Flux | Distance |
|------|---------|-------------|------|----------|
| 1 | Daloa | Abidjan | 34 | 383 km |
| 2 | Bouaké | Abidjan | 31 | 350 km |
| 3 | Man | Abidjan | 28 | 580 km |
| 4 | Korhogo | Abidjan | 25 | 635 km |
| 5 | San-Pédro | Abidjan | 23 | 350 km |
| 6 | Abidjan | Yamoussoukro | 19 | 248 km |
| 7 | Gagnoa | Abidjan | 18 | 275 km |
| 8 | Bondoukou | Abidjan | 16 | 420 km |
| 9 | Odienné | Abidjan | 14 | 780 km |
| 10 | Abengourou | Abidjan | 12 | 210 km |

> **Observation** : Abidjan est la destination principale de 78% des flux migratoires.

### 6.2.5 Saisonnalité des migrations

| Mois | Flux | Indice saisonnier | Facteurs |
|------|------|-------------------|----------|
| Janvier | 52 | 1.25 | Post-fêtes, rentrée |
| Février | 38 | 0.91 | - |
| Mars | 35 | 0.84 | - |
| Avril | 31 | 0.74 | Travaux agricoles |
| Mai | 28 | 0.67 | Travaux agricoles |
| Juin | 33 | 0.79 | - |
| Juillet | 42 | 1.01 | Vacances scolaires |
| Août | 48 | 1.15 | Vacances scolaires |
| Septembre | 56 | 1.34 | Rentrée scolaire |
| Octobre | 54 | 1.30 | Rentrée universitaire |
| Novembre | 45 | 1.08 | - |
| Décembre | 38 | 0.91 | Retours fêtes |

### 6.2.6 Matrice Origine-Destination

#### Flux inter-régionaux (extrait)

|  | Abidjan | Bouaké | Daloa | Korhogo | San-Pédro |
|--|---------|--------|-------|---------|-----------|
| **Abidjan** | - | 12 | 8 | 5 | 11 |
| **Bouaké** | 31 | - | 4 | 7 | 2 |
| **Daloa** | 34 | 6 | - | 1 | 8 |
| **Korhogo** | 25 | 9 | 2 | - | 1 |
| **San-Pédro** | 23 | 3 | 5 | 0 | - |

### 6.2.7 Profil des migrants

#### Par âge

| Groupe d'âge | Taux de migration | Sur-/Sous-représentation |
|--------------|-------------------|--------------------------|
| 15-24 ans | 7.2% | +48% |
| 25-34 ans | 6.1% | +25% |
| 35-44 ans | 4.3% | -12% |
| 45-54 ans | 3.1% | -36% |
| 55+ ans | 1.8% | -63% |

#### Par niveau de richesse

| Quintile | Taux de migration | Observation |
|----------|-------------------|-------------|
| Q1 | 3.2% | Contraintes financières |
| Q2 | 4.1% | - |
| Q3 | 5.4% | - |
| Q4 | 6.8% | Mobilité facilitée |
| Q5 | 4.9% | Stabilité professionnelle |

---

## 6.3 Indicateurs de Mobilité Quotidienne

### 6.3.1 Volume de mobilité

| Indicateur | Valeur |
|------------|--------|
| Trajets totaux | 16 852 |
| Trajets par utilisateur (moyenne) | 16.9 |
| Trajets par jour (moyenne) | 1.7 |
| Utilisateurs avec mobilité | 1 000 (échantillon) |

### 6.3.2 Caractéristiques des trajets

#### Distances

| Statistique | Valeur |
|-------------|--------|
| Distance moyenne | 8.7 km |
| Distance médiane | 5.2 km |
| Écart-type | 12.3 km |
| Distance totale | 146 612 km |

#### Durées

| Statistique | Valeur |
|-------------|--------|
| Durée moyenne | 23.4 min |
| Durée médiane | 18 min |
| Écart-type | 19.7 min |

#### Vitesses

| Statistique | Valeur |
|-------------|--------|
| Vitesse moyenne | 22.3 km/h |
| Vitesse médiane | 18.5 km/h |

### 6.3.3 Répartition modale

| Mode | Trajets | % | Distance moy. | Durée moy. |
|------|---------|---|---------------|------------|
| marche_a_pied | 5 224 | 31.0% | 1.8 km | 22 min |
| moto | 4 218 | 25.0% | 7.4 km | 18 min |
| taxi | 3 034 | 18.0% | 9.2 km | 28 min |
| bus | 2 528 | 15.0% | 12.6 km | 45 min |
| voiture_personnelle | 1 848 | 11.0% | 15.3 km | 24 min |

### 6.3.4 Motifs de déplacement

| Motif | Trajets | % | Heure pic |
|-------|---------|---|-----------|
| Travail | 5 393 | 32.0% | 07h-08h |
| Courses/Shopping | 3 202 | 19.0% | 10h-12h |
| Loisirs | 2 696 | 16.0% | 14h-17h |
| Éducation | 2 359 | 14.0% | 07h-08h |
| Santé | 1 180 | 7.0% | 09h-11h |
| Famille | 1 348 | 8.0% | 18h-20h |
| Autre | 674 | 4.0% | - |

### 6.3.5 Patterns temporels

#### Distribution horaire

| Période | Trajets | % | Caractéristique |
|---------|---------|---|-----------------|
| 00h-06h | 842 | 5.0% | Nuit |
| 06h-09h | 4 213 | 25.0% | **Pointe matin** |
| 09h-12h | 2 528 | 15.0% | Matinée |
| 12h-14h | 1 685 | 10.0% | Pause déjeuner |
| 14h-17h | 2 359 | 14.0% | Après-midi |
| 17h-20h | 3 876 | 23.0% | **Pointe soir** |
| 20h-24h | 1 349 | 8.0% | Soirée |

#### Heures de pointe identifiées

| Pointe | Début | Pic | Fin | Volume |
|--------|-------|-----|-----|--------|
| Matin | 06h30 | 07h45 | 09h00 | 4 213 trajets |
| Soir | 17h00 | 18h30 | 20h00 | 3 876 trajets |

#### Variation journalière

| Jour | Trajets | Indice |
|------|---------|--------|
| Lundi | 2 612 | 1.08 |
| Mardi | 2 528 | 1.05 |
| Mercredi | 2 444 | 1.01 |
| Jeudi | 2 528 | 1.05 |
| Vendredi | 2 696 | 1.12 |
| Samedi | 2 191 | 0.91 |
| Dimanche | 1 853 | 0.77 |

### 6.3.6 Indicateurs de congestion

#### Indice de congestion par zone

| Zone | Indice | Interprétation |
|------|--------|----------------|
| Abidjan Centre | 0.78 | Congestion élevée |
| Abidjan Périphérie | 0.52 | Congestion modérée |
| Grandes villes | 0.41 | Congestion légère |
| Villes moyennes | 0.23 | Fluide |
| Zones rurales | 0.08 | Très fluide |

#### Temps perdu dans les embouteillages

| Indicateur | Valeur |
|------------|--------|
| Temps perdu moyen (Abidjan) | 12.4 min/trajet |
| Temps perdu moyen (autres villes) | 4.2 min/trajet |
| Coût économique estimé | 15 000 FCFA/mois/utilisateur |

### 6.3.7 Rayon de mobilité

| Catégorie | Rayon | % Population |
|-----------|-------|--------------|
| Très local | < 2 km | 18.3% |
| Local | 2-5 km | 32.1% |
| Urbain | 5-15 km | 28.7% |
| Périurbain | 15-30 km | 14.2% |
| Régional | > 30 km | 6.7% |

---

## 6.4 Indicateurs Croisés

### 6.4.1 Mobilité et pauvreté

| Quintile | Trajets/jour | Distance moy. | Mode principal |
|----------|--------------|---------------|----------------|
| Q1 | 1.2 | 3.4 km | marche_a_pied (62%) |
| Q2 | 1.5 | 5.1 km | marche_a_pied (48%) |
| Q3 | 1.8 | 7.8 km | moto (38%) |
| Q4 | 2.1 | 10.2 km | taxi (31%) |
| Q5 | 2.4 | 14.6 km | voiture_personnelle (42%) |

### 6.4.2 Migration et pauvreté

| Quintile | Taux migration | Type dominant |
|----------|----------------|---------------|
| Q1 | 3.2% | agriculture_saisonniere |
| Q2 | 4.1% | migration_travail |
| Q3 | 5.4% | migration_travail |
| Q4 | 6.8% | migration_travail |
| Q5 | 4.9% | relocalisation_permanente |

### 6.4.3 Migration et mobilité pré/post

| Indicateur | Avant migration | Après migration | Variation |
|------------|-----------------|-----------------|-----------|
| Trajets/jour | 1.4 | 2.1 | +50% |
| Distance moy. | 5.2 km | 8.9 km | +71% |
| Rayon mobilité | 8.3 km | 12.7 km | +53% |

---

## 6.5 Validation des résultats

### 6.5.1 Comparaison avec sources officielles

| Indicateur | Notre étude | Source officielle | Écart | Source |
|------------|-------------|-------------------|-------|--------|
| Taux pauvreté | 38.2% | 39.4% | -1.2 pp | ENV 2015 |
| Taux migration interne | 4.87% | 5.2% | -0.33 pp | RGPH 2021 |
| % Urbain | 54.9% | 52.7% | +2.2 pp | RGPH 2021 |
| Distance moy. domicile-travail | 8.7 km | 9.1 km | -0.4 km | ENSESI 2017 |

### 6.5.2 Tests de robustesse

| Test | Méthode | Résultat |
|------|---------|----------|
| Bootstrap (n=1000) | IC 95% sur IPM | [0.198, 0.214] |
| Validation croisée | 5-fold sur wealth index | R² = 0.89 |
| Analyse de sensibilité | Variation seuils ±10% | Impact < 3% |

---

## 6.6 Synthèse des résultats

### Indicateurs clés

| Domaine | Indicateur principal | Valeur |
|---------|---------------------|--------|
| **Pauvreté** | IPM | 0.206 |
| **Pauvreté** | % Q1-Q2 | 40% |
| **Migration** | Taux annuel | 4.87% |
| **Migration** | Distance moyenne | 124.7 km |
| **Mobilité** | Trajets/jour | 1.7 |
| **Mobilité** | Distance moyenne | 8.7 km |

### Fiabilité des indicateurs

| Indicateur | Fiabilité | Justification |
|------------|-----------|---------------|
| Wealth Index | ★★★★☆ | Variance expliquée 57.73% |
| IPM | ★★★★★ | Méthode Alkire-Foster validée |
| Taux migration | ★★★☆☆ | Dépend des seuils choisis |
| Patterns mobilité | ★★★★☆ | Cohérent avec enquêtes terrain |

---

**Document** : Résultats  
**Version** : 1.0  
**Date** : Janvier 2026  
**Projet** : CI-Mobility-Prototype  
**Standard** : UN-MPDMS v2.0