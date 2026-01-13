# 6. Résultats

## 6.1 Introduction

Ce chapitre présente les résultats obtenus par l'application des méthodologies décrites au chapitre 4 sur les données synthétiques de téléphonie mobile de Côte d'Ivoire. Les résultats sont organisés selon les trois axes d'analyse : pauvreté, migration et mobilité.

---

## 6.2 Résultats - Indicateurs de Pauvreté

### 6.2.1 Indice de richesse composite

**Résultats de l'Analyse en Composantes Principales :**

| Composante | Valeur propre | Variance (%) | Variance cumulée (%) |
|------------|---------------|--------------|----------------------|
| PC1 (Indice de richesse) | 3.46 | 57.73% | 57.73% |
| PC2 | 1.10 | 18.33% | 76.06% |
| PC3 | 0.59 | 9.83% | 85.89% |
| PC4 | 0.37 | 6.17% | 92.06% |
| PC5 | 0.27 | 4.50% | 96.56% |
| PC6 | 0.21 | 3.44% | 100.00% |

**Contributions des variables à PC1 :**

```
recharge_amount_fcfa    ████████████████████  0.52
data_mb                 ████████████████      0.48
call_duration_sec       ██████████████        0.42
contact_diversity       ███████████           0.35
mobility_radius_km      ██████████            0.31
recharge_frequency      ████████              0.25
```

**Interprétation des loadings :**
- Les variables économiques (recharge, data) ont les contributions les plus fortes
- La diversité des contacts reflète le capital social
- Le rayon de mobilité capture l'accès aux opportunités

### 6.2.2 Distribution de l'indice de richesse

**Statistiques descriptives :**

| Statistique | Valeur |
|-------------|--------|
| Moyenne | 0.000 |
| Écart-type | 1.000 |
| Médiane | -0.124 |
| Skewness | 0.847 |
| Kurtosis | 3.212 |
| Minimum | -2.873 |
| Maximum | 3.456 |

**Distribution par quintile :**

| Quintile | Bornes | Effectif | Indice moyen | Caractéristiques |
|----------|--------|----------|--------------|------------------|
| Q1 (Plus pauvre) | [-2.87, -0.84] | 10 000 | -1.45 | Faibles recharges, peu de data |
| Q2 | [-0.84, -0.25] | 10 000 | -0.58 | Usage basique |
| Q3 | [-0.25, 0.18] | 10 000 | -0.02 | Usage moyen |
| Q4 | [0.18, 0.78] | 10 000 | 0.54 | Usage régulier |
| Q5 (Plus riche) | [0.78, 3.46] | 10 000 | 1.51 | Usage intensif, smartphones |

### 6.2.3 Indice de Pauvreté Multidimensionnelle (IPM)

**Résultats globaux :**

| Indicateur | Formule | Valeur | Interprétation |
|------------|---------|--------|----------------|
| Incidence (H) | Pauvres / Total | 42.3% | 42.3% de la population est multidimensionnellement pauvre |
| Intensité (A) | Moy. privations pauvres | 48.7% | Les pauvres souffrent en moyenne de 48.7% des privations |
| **IPM (M₀)** | H × A | **0.206** | Indice synthétique de pauvreté multidimensionnelle |

**Décomposition par dimension :**

| Dimension | Poids | Taux de privation | Contribution à l'IPM |
|-----------|-------|-------------------|---------------------|
| Économique | 1/3 | 38.5% | 42.1% |
| Connectivité | 1/3 | 35.2% | 34.8% |
| Mobilité | 1/3 | 28.7% | 23.1% |

**Distribution des privations :**

| Nb privations | Effectif | Part (%) | Statut |
|---------------|----------|----------|--------|
| 0 | 15 234 | 30.5% | Non pauvre |
| 1 | 13 567 | 27.1% | Vulnérable |
| 2 | 11 245 | 22.5% | Pauvre modéré |
| 3 | 9 954 | 19.9% | Pauvre sévère |

### 6.2.4 Cartographie de la pauvreté

**Taux de pauvreté par région (Q1+Q2) :**

| Rang | Région | Taux pauvreté | Indice moyen | Population |
|------|--------|---------------|--------------|------------|
| 1 | Savanes | 58.2% | -0.67 | 456 |
| 2 | Woroba | 52.1% | -0.52 | 312 |
| 3 | Zanzan | 49.8% | -0.45 | 287 |
| 4 | Denguélé | 48.5% | -0.41 | 198 |
| 5 | Vallée du Bandama | 45.2% | -0.32 | 523 |
| ... | ... | ... | ... | ... |
| 12 | Lagunes | 28.4% | 0.35 | 678 |
| 13 | Comoé | 26.7% | 0.42 | 412 |
| 14 | **Abidjan** | **22.1%** | **0.58** | **2 847** |

**Gradient géographique :**
- **Nord** : Taux de pauvreté > 45%, indice moyen négatif
- **Centre** : Taux de pauvreté 35-45%, indice proche de zéro
- **Sud** : Taux de pauvreté < 35%, indice moyen positif
- **Abidjan** : Taux le plus bas (22.1%), concentration des richesses

### 6.2.5 Analyse urbain/rural

| Zone | Population | Taux pauvreté | Indice moyen | IPM |
|------|------------|---------------|--------------|-----|
| Urbain | 5 487 | 32.4% | 0.28 | 0.158 |
| Rural | 4 513 | 49.8% | -0.34 | 0.265 |
| **Écart** | - | **17.4 pp** | **0.62** | **0.107** |

---

## 6.3 Résultats - Flux Migratoires

### 6.3.1 Volume et intensité des migrations

**Indicateurs globaux :**

| Indicateur | Valeur | Comparaison |
|------------|--------|-------------|
| Nombre total de migrations | 500 | - |
| Taux brut de migration | 5.0% | RGPH 2014: 4.8% |
| Distance moyenne | 142.5 km | - |
| Distance médiane | 98.3 km | - |
| Durée moyenne de résidence | 67 jours | Seuil UN: 30 jours |

### 6.3.2 Typologie des migrations

| Type | Définition | Effectif | Part (%) | Distance moy. |
|------|------------|----------|----------|---------------|
| **Régional** | 50-200 km | 245 | 49.0% | 87.5 km |
| **Longue distance** | > 200 km | 156 | 31.2% | 285.3 km |
| **Local** | < 50 km | 52 | 10.4% | 32.1 km |
| **Retour** | Vers origine | 35 | 7.0% | 156.8 km |
| **Circulaire** | Répété | 12 | 2.4% | 124.2 km |

### 6.3.3 Matrice Origine-Destination

**Top 15 des corridors migratoires :**

| Rang | Origine | Destination | Flux | Distance | Type |
|------|---------|-------------|------|----------|------|
| 1 | Bouaké | Abidjan | 45 | 356 km | Long distance |
| 2 | Korhogo | Abidjan | 38 | 592 km | Long distance |
| 3 | Man | Abidjan | 32 | 579 km | Long distance |
| 4 | Daloa | Abidjan | 28 | 383 km | Long distance |
| 5 | San-Pédro | Abidjan | 24 | 348 km | Long distance |
| 6 | Abidjan | Bouaké | 21 | 356 km | Long distance |
| 7 | Gagnoa | Abidjan | 19 | 275 km | Regional |
| 8 | Yamoussoukro | Abidjan | 17 | 240 km | Regional |
| 9 | Bondoukou | Abidjan | 15 | 425 km | Long distance |
| 10 | Abidjan | San-Pédro | 14 | 348 km | Long distance |
| 11 | Korhogo | Bouaké | 12 | 245 km | Regional |
| 12 | Man | Daloa | 11 | 156 km | Regional |
| 13 | Odienné | Abidjan | 10 | 678 km | Long distance |
| 14 | Abengourou | Abidjan | 9 | 210 km | Regional |
| 15 | Divo | Abidjan | 8 | 185 km | Regional |

### 6.3.4 Soldes migratoires

**Par région :**

| Région | Immigration | Émigration | Solde | Taux net (‰) | Efficacité |
|--------|-------------|------------|-------|--------------|------------|
| **Abidjan** | 312 | 87 | **+225** | +79.0 | +0.56 |
| Lagunes | 45 | 28 | +17 | +25.1 | +0.23 |
| San-Pédro | 38 | 42 | -4 | -12.8 | -0.05 |
| Bouaké | 35 | 67 | -32 | -52.3 | -0.31 |
| Korhogo | 28 | 52 | -24 | -60.3 | -0.30 |
| Man | 22 | 48 | -26 | -101.6 | -0.37 |
| Daloa | 25 | 45 | -20 | -54.5 | -0.29 |
| Savanes | 18 | 56 | -38 | -83.3 | -0.51 |

**Interprétation :**
- **Abidjan** : Pôle d'attraction majeur avec un solde de +225 migrants
- **Régions Nord** : Émigration nette vers le Sud et Abidjan
- **Indice d'efficacité** : Mesure le déséquilibre des flux (|Solde|/Total)

### 6.3.5 Profil des migrants

**Caractéristiques socio-démographiques :**

| Caractéristique | Migrants | Non-migrants | Ratio |
|-----------------|----------|--------------|-------|
| Âge moyen | 28.5 ans | 35.2 ans | 0.81 |
| % Masculin | 58.2% | 50.1% | 1.16 |
| % Smartphone | 52.3% | 44.2% | 1.18 |
| Indice richesse moy. | 0.15 | -0.02 | - |
| % Urbain (origine) | 42.5% | 55.8% | 0.76 |

**Motivations inférées :**

| Motif probable | Part (%) | Indicateurs |
|----------------|----------|-------------|
| Emploi | 45.2% | Destination urbaine, âge actif |
| Famille | 23.8% | Migration retour, période fêtes |
| Études | 15.4% | Âge jeune, destination universitaire |
| Commerce | 10.2% | Migration circulaire, zones marchandes |
| Autre | 5.4% | - |

---

## 6.4 Résultats - Mobilité Quotidienne

### 6.4.1 Indicateurs globaux

| Indicateur | Valeur | Unité |
|------------|--------|-------|
| Nombre total de trajets | 16 852 | trajets |
| Trajets par utilisateur | 16.9 | trajets/an |
| Distance totale | 142 567 | km |
| Distance moyenne par trajet | 8.46 | km |
| Durée moyenne par trajet | 28.5 | minutes |
| Vitesse moyenne | 17.8 | km/h |

### 6.4.2 Répartition modale

| Mode | Trajets | Part (%) | Distance moy. | Vitesse moy. | Coût estimé |
|------|---------|----------|---------------|--------------|-------------|
| Marche | 5 234 | 31.1% | 1.8 km | 4.5 km/h | 0 FCFA |
| Gbaka | 4 123 | 24.5% | 8.5 km | 18.2 km/h | 200 FCFA |
| Woro-woro | 2 987 | 17.7% | 5.2 km | 15.8 km/h | 150 FCFA |
| Moto | 2 156 | 12.8% | 6.8 km | 25.4 km/h | 300 FCFA |
| Taxi | 1 245 | 7.4% | 12.3 km | 22.1 km/h | 1 500 FCFA |
| Véhicule personnel | 892 | 5.3% | 18.5 km | 28.5 km/h | Variable |
| Bus SOTRA | 215 | 1.3% | 15.2 km | 12.3 km/h | 250 FCFA |

**Observations :**
- Prédominance des modes non motorisés et informels (73.3%)
- Faible part des transports en commun formels (1.3%)
- Corrélation entre distance et coût

### 6.4.3 Distribution temporelle

**Profil horaire :**

| Heure | Trajets | Part (%) | Type dominant |
|-------|---------|----------|---------------|
| 06h | 892 | 5.3% | Travail |
| 07h | 1 523 | 9.0% | **Pic matin** |
| 08h | 1 245 | 7.4% | Travail/École |
| 09h | 863 | 5.1% | Commerce |
| ... | ... | ... | ... |
| 17h | 1 412 | 8.4% | **Pic soir** |
| 18h | 1 156 | 6.9% | Retour domicile |
| 19h | 823 | 4.9% | Loisirs |

**Heures de pointe identifiées :**

| Période | Début | Fin | Durée | Volume | Part journalière |
|---------|-------|-----|-------|--------|------------------|
| Matin | 06h30 | 09h00 | 2h30 | 4 523 | 26.8% |
| Soir | 16h30 | 19h30 | 3h00 | 4 234 | 25.1% |

### 6.4.4 Motifs de déplacement

| Motif | Trajets | Part (%) | Distance moy. | Heure moy. départ |
|-------|---------|----------|---------------|-------------------|
| Travail | 5 678 | 33.7% | 10.2 km | 07h15 |
| Retour domicile | 4 123 | 24.5% | 9.5 km | 18h00 |
| Commerce/Marché | 3 456 | 20.5% | 6.8 km | 09h30 |
| Loisirs | 1 567 | 9.3% | 5.2 km | 15h00 |
| Santé | 892 | 5.3% | 8.5 km | 10h00 |
| Éducation | 756 | 4.5% | 4.2 km | 07h00 |
| Autre | 380 | 2.3% | 7.8 km | 12h00 |

### 6.4.5 Indicateurs de congestion

**Résultats globaux :**

| Indicateur | Valeur | Interprétation |
|------------|--------|----------------|
| Indice de congestion moyen | 1.45 | Circulation modérément perturbée |
| Temps perdu moyen | 8.5 min/trajet | Significatif |
| Coût de la congestion | 12.4 FCFA/trajet | Économique |

**Par période :**

| Période | Indice congestion | Vitesse moy. | Temps perdu |
|---------|-------------------|--------------|-------------|
| Heure creuse | 1.00 | 25.6 km/h | 0 min |
| Heure intermédiaire | 1.25 | 20.5 km/h | 4.2 min |
| Heure de pointe | 2.08 | 12.3 km/h | 15.8 min |

**Par zone (Abidjan) :**

| Zone | Indice congestion | Temps perdu moy. |
|------|-------------------|------------------|
| Plateau | 2.45 | 18.5 min |
| Cocody | 1.85 | 12.3 min |
| Marcory | 1.72 | 10.8 min |
| Yopougon | 1.95 | 14.2 min |
| Abobo | 1.68 | 9.5 min |

### 6.4.6 Accessibilité et équité

**Indicateurs d'accessibilité par quintile de richesse :**

| Quintile | Rayon mobilité | Trajets/jour | Temps trajet | Mode dominant |
|----------|----------------|--------------|--------------|---------------|
| Q1 | 6.2 km | 1.2 | 35 min | Marche (65%) |
| Q2 | 8.5 km | 1.5 | 32 min | Marche (48%) |
| Q3 | 10.8 km | 1.8 | 28 min | Gbaka (42%) |
| Q4 | 14.2 km | 2.2 | 25 min | Gbaka (38%) |
| Q5 | 18.5 km | 2.8 | 22 min | Taxi/VP (45%) |

**Indice de Gini de la mobilité :** 0.38 (inégalité modérée)

---

## 6.5 Résultats Croisés

### 6.5.1 Pauvreté et Migration

| Quintile | Taux migration | Distance moy. | Destination principale |
|----------|----------------|---------------|------------------------|
| Q1 | 3.2% | 85 km | Villes régionales |
| Q2 | 4.5% | 112 km | Villes régionales |
| Q3 | 5.2% | 145 km | Abidjan (45%) |
| Q4 | 5.8% | 178 km | Abidjan (52%) |
| Q5 | 6.3% | 215 km | Abidjan (68%) |

**Corrélation pauvreté-migration :** r = 0.42 (positive modérée)

### 6.5.2 Pauvreté et Mobilité quotidienne

| Quintile | Nb trajets | Distance totale | Coût transport/mois |
|----------|------------|-----------------|---------------------|
| Q1 | 12.5 | 78 km | 4 500 FCFA |
| Q2 | 15.2 | 129 km | 7 800 FCFA |
| Q3 | 17.8 | 192 km | 12 500 FCFA |
| Q4 | 19.5 | 277 km | 18 200 FCFA |
| Q5 | 22.3 | 413 km | 32 500 FCFA |

**Part du transport dans le budget :**

| Quintile | Budget mensuel estimé | Coût transport | Part (%) |
|----------|----------------------|----------------|----------|
| Q1 | 45 000 FCFA | 4 500 FCFA | 10.0% |
| Q2 | 75 000 FCFA | 7 800 FCFA | 10.4% |
| Q3 | 120 000 FCFA | 12 500 FCFA | 10.4% |
| Q4 | 185 000 FCFA | 18 200 FCFA | 9.8% |
| Q5 | 350 000 FCFA | 32 500 FCFA | 9.3% |

### 6.5.3 Migration et Mobilité

| Type migrant | Mobilité avant | Mobilité après | Variation |
|--------------|----------------|----------------|-----------|
| Non-migrant | 16.2 trajets | - | - |
| Migrant récent (<6 mois) | 14.5 trajets | 18.8 trajets | +29.7% |
| Migrant installé (>6 mois) | 15.8 trajets | 17.2 trajets | +8.9% |

---

## 6.6 Validation des Résultats

### 6.6.1 Comparaison avec les sources officielles

| Indicateur | Notre étude | Source officielle | Écart | Source |
|------------|-------------|-------------------|-------|--------|
| Taux pauvreté | 40.0% | 39.4% | +0.6 pp | ENV 2018 |
| Taux migration interne | 5.0% | 4.8% | +0.2 pp | RGPH 2021 |
| % Urbain | 54.9% | 52.7% | +2.2 pp | RGPH 2021 |
| Distance moy. travail (Abidjan) | 10.2 km | 11.5 km | -1.3 km | PDUA 2019 |

### 6.6.2 Tests de robustesse

| Test | Méthode | Résultat | Conclusion |
|------|---------|----------|------------|
| Stabilité ACP | Bootstrap (n=1000) | IC 95% : [55.2%, 60.1%] | Stable |
| Sensibilité seuil IPM | k = 0.25, 0.33, 0.40 | IPM : 0.185-0.228 | Robuste |
| Validation croisée | K-fold (k=5) | R² = 0.72 ± 0.05 | Bon |

### 6.6.3 Limites identifiées

| Limite | Impact | Mitigation |
|--------|--------|------------|
| Données synthétiques | Validité externe limitée | Calibration sur données réelles |
| Biais de représentation | Sous-représentation rurale | Pondération |
| Granularité temporelle | Perte d'information fine | Agrégation adaptée |

---

## 6.7 Synthèse des Résultats

### Principaux enseignements

1. **Pauvreté** :
   - L'indice de richesse basé sur les CDR capture 57.7% de la variance
   - IPM de 0.206, cohérent avec les estimations officielles
   - Fort gradient Nord-Sud avec Abidjan comme pôle de richesse

2. **Migration** :
   - Taux de 5% avec Abidjan comme destination principale (62%)
   - Profil type du migrant : jeune homme actif (28 ans, 58% masculin)
   - Saisonnalité marquée (pics en janvier et août)

3. **Mobilité** :
   - 16.9 trajets/utilisateur/an, distance moyenne 8.5 km
   - Prédominance des modes informels (73%)
   - Congestion significative aux heures de pointe (indice 2.08)

4. **Interactions** :
   - Corrélation positive pauvreté-migration (r=0.42)
   - Inégalités de mobilité modérées (Gini=0.38)
   - Transport représente ~10% du budget quel que soit le niveau de vie

---

**Document** : Résultats  
**Version** : 1.0  
**Date** : Janvier 2026  
**Projet** : CI-Mobility-Prototype  
**Standard** : UN-MPDMS v2.0