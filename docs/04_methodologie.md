# 4. Méthodologie

## 4.1 Approche générale

### 4.1.1 Pipeline de traitement

Le projet implémente un pipeline de traitement en 4 étapes :

### 4.1.2 Principes méthodologiques

| Principe | Description |
|----------|-------------|
| **Reproductibilité** | Seed fixe pour génération aléatoire |
| **Modularité** | Composants indépendants et réutilisables |
| **Transparence** | Code source documenté et ouvert |
| **Standards** | Conformité UN-MPDMS v2.0 |

## 4.2 Calcul de l'indice de pauvreté

### 4.2.1 Contexte et justification

L'estimation de la pauvreté à partir des données de téléphonie mobile repose sur l'hypothèse que les comportements d'utilisation du téléphone reflètent, au moins partiellement, le statut socio-économique des individus.

**Littérature de référence :**
- Blumenstock et al. (2015) : Prédiction de la richesse au Rwanda
- Steele et al. (2017) : Cartographie de la pauvreté au Bangladesh
- Pokhriyal & Jacques (2017) : Estimation multidimensionnelle

### 4.2.2 Variables utilisées

Les variables sélectionnées pour le calcul de l'indice de richesse sont :

| Variable | Poids attendu | Justification |
|----------|---------------|---------------|
| `recharge_amount_fcfa` | Fort (+) | Capacité de dépense directe |
| `call_duration_sec` | Modéré (+) | Utilisation des services |
| `data_mb` | Fort (+) | Accès numérique et smartphone |
| `contact_diversity_score` | Modéré (+) | Capital social |
| `mobility_radius_km` | Modéré (+) | Accès aux transports |
| `recharge_frequency_weekly` | Faible (+) | Régularité des revenus |

### 4.2.3 Méthode : Analyse en Composantes Principales (ACP)

#### Pourquoi l'ACP ?

1. **Réduction de dimensionnalité** : Synthétise plusieurs variables corrélées
2. **Objectivité** : Pondérations déterminées par les données
3. **Interprétabilité** : Premier axe = gradient de richesse
4. **Standard DHS** : Méthode utilisée pour l'Asset Index

#### Algorithme

**Étape 1 : Standardisation**

Pour chaque variable $X_j$ :

$$Z_j = \frac{X_j - \mu_j}{\sigma_j}$$

où $\mu_j$ est la moyenne et $\sigma_j$ l'écart-type.

**Étape 2 : Calcul de la matrice de corrélation**

$$R = \frac{1}{n-1} Z^T Z$$

**Étape 3 : Extraction des composantes principales**

Décomposition en valeurs propres : $R = V \Lambda V^T$

**Étape 4 : Calcul de l'indice**

L'indice de richesse est le score sur la première composante principale :

$$WI_i = \sum_{j=1}^{p} w_j \cdot Z_{ij}$$

où $w_j$ sont les loadings de PC1.

#### Paramètres

| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| Composantes retenues | 1 (PC1) | Variance > 50% |
| Standardisation | Z-score | Échelles comparables |
| Traitement NA | Imputation médiane | Robustesse |

### 4.2.4 Attribution des quintiles

Les quintiles de richesse sont attribués selon les percentiles :

| Quintile | Percentiles | Interprétation |
|----------|-------------|----------------|
| Q1 (Plus pauvre) | 0 - 20% | Pauvreté extrême |
| Q2 | 20 - 40% | Pauvreté modérée |
| Q3 | 40 - 60% | Classe moyenne inférieure |
| Q4 | 60 - 80% | Classe moyenne supérieure |
| Q5 (Plus riche) | 80 - 100% | Aisé |

### 4.2.5 Indice de Pauvreté Multidimensionnelle (IPM)

#### Méthode Alkire-Foster

L'IPM est calculé selon la méthode d'Alkire-Foster (2011), standard international utilisé par le PNUD.

**Dimensions et indicateurs :**

| Dimension | Poids | Indicateur | Seuil de privation |
|-----------|-------|------------|-------------------|
| **Économique** | 1/3 | Recharges | < percentile 20 |
| **Connectivité** | 1/3 | Données mobiles | < 100 Mo/mois |
| **Social** | 1/3 | Diversité contacts | < 0.3 |

**Formule de l'IPM :**

$$IPM = H \times A$$

où :
- $H$ = Incidence (proportion de pauvres)
- $A$ = Intensité (profondeur moyenne des privations)

**Score individuel :**

$$c_i = \sum_{d=1}^{D} w_d \cdot \mathbb{1}_{privé}(i, d)$$

Un individu est considéré pauvre multidimensionnel si $c_i \geq k$ (seuil k = 0.33).

## 4.3 Détection des migrations

### 4.3.1 Définition UN-MPDMS

Selon le standard UN-MPDMS, une **migration interne** est définie comme :

> "Un changement de résidence habituelle d'une unité administrative à une autre, à l'intérieur des frontières nationales, pour une durée minimale spécifiée."

### 4.3.2 Algorithme de détection

#### Étape 1 : Identification du domicile

Le domicile est détecté par l'analyse des positions nocturnes (22h - 6h) :

#### Étape 2 : Détection des changements

#### Étape 3 : Classification

| Type | Critères |
|------|----------|
| `long_distance` | Distance > 200 km |
| `regional` | 50 km < Distance ≤ 200 km |
| `local` | Distance ≤ 50 km |
| `return` | Destination = origine précédente |
| `seasonal` | Pattern saisonnier détecté |
| `circular` | Aller-retour répété |

### 4.3.3 Paramètres

| Paramètre | Valeur par défaut | Plage recommandée |
|-----------|-------------------|-------------------|
| `distance_threshold_km` | 50 | 30 - 100 |
| `duration_threshold_days` | 30 | 14 - 90 |
| `confidence_threshold` | 0.7 | 0.5 - 0.9 |
| `night_hours` | 22h - 6h | 21h - 7h |

### 4.3.4 Calcul des flux migratoires

La matrice origine-destination (O-D) est calculée comme :

$$F_{ij} = \sum_{u} \mathbb{1}_{migration}(u, i \rightarrow j)$$

où $F_{ij}$ est le flux de la région $i$ vers la région $j$.

**Indicateurs dérivés :**

| Indicateur | Formule | Description |
|------------|---------|-------------|
| Taux d'émigration | $E_i = \frac{\sum_j F_{ij}}{P_i}$ | Part de la population qui émigre |
| Taux d'immigration | $I_j = \frac{\sum_i F_{ij}}{P_j}$ | Part de nouveaux arrivants |
| Solde migratoire | $S_i = \sum_j F_{ji} - \sum_j F_{ij}$ | Balance entrées/sorties |
| Efficacité migratoire | $ME_i = \frac{S_i}{I_i + E_i}$ | Direction nette des flux |

## 4.4 Analyse de la mobilité quotidienne

### 4.4.1 Reconstruction des trajets

Les trajets sont reconstruits à partir des séquences de connexions aux antennes :

### 4.4.2 Inférence du mode de transport

Le mode de transport est inféré à partir de la vitesse moyenne :

| Mode | Vitesse min | Vitesse max | Conditions |
|------|-------------|-------------|------------|
| `walking` | 0 | 6 km/h | - |
| `bicycle` | 6 | 20 km/h | Distance < 10 km |
| `gbaka` | 10 | 30 km/h | Zone urbaine |
| `taxi` | 15 | 40 km/h | - |
| `personal_vehicle` | 20 | 80 km/h | - |
| `bus` | 10 | 35 km/h | Heure de pointe |

### 4.4.3 Métriques de mobilité

| Métrique | Formule | Unité |
|----------|---------|-------|
| Distance totale | $D_u = \sum_t d_t$ | km/jour |
| Nombre de trajets | $N_u = count(trajets)$ | trajets/jour |
| Rayon de giration | $r_g = \sqrt{\frac{1}{N}\sum_i (r_i - r_{cm})^2}$ | km |
| Entropie spatiale | $H = -\sum_i p_i \log p_i$ | bits |
| Régularité | $Reg = \frac{f_{top3}}{\sum_i f_i}$ | [0-1] |

### 4.4.4 Détection des heures de pointe

Les heures de pointe sont identifiées par analyse de la distribution horaire :

| Critère | Description |
|---------|-------------|
| Fréquence | Nombre de connexions |
| Amplitude | Plage horaire étendue |
| Régularité | Modèle récurrent |

## 4.5 Agrégation spatiale

### 4.5.1 Niveaux d'agrégation

| Niveau | Résolution H3 | Aire | Usage |
|--------|---------------|------|-------|
| National | - | 322 463 km² | Totaux |
| Régional | 5 | ~253 km² | Comparaisons |
| Départemental | 6 | ~36 km² | Planification |
| Local | 8 | ~0.74 km² | Analyse fine |

### 4.5.2 Méthodes d'agrégation

| Indicateur | Méthode | Justification |
|------------|---------|---------------|
| Population | Somme | Comptage |
| Indice richesse | Moyenne pondérée | Représentativité |
| Taux de pauvreté | Ratio | Proportion |
| Flux migration | Somme | Comptage |
| Distance moyenne | Moyenne | Tendance centrale |

### 4.5.3 Pondération spatiale

Pour corriger les biais de représentativité :

$$\hat{\theta}_{zone} = \frac{\sum_i w_i \cdot \theta_i}{\sum_i w_i}$$

où $w_i$ est le poids de l'utilisateur $i$ basé sur le taux de pénétration mobile de sa zone.

## 4.6 Validation

### 4.6.1 Validation croisée

| Source de validation | Indicateur comparé |
|---------------------|-------------------|
| ENV 2020 | Taux de pauvreté régional |
| RGPH 2021 | Répartition spatiale population |
| Enquête transport | Parts modales |
| Données ARTCI | Flux de communication |

### 4.6.2 Métriques de validation

| Métrique | Formule | Seuil acceptable |
|----------|---------|------------------|
| Corrélation | $r_{Pearson}$ | > 0.7 |
| RMSE | $\sqrt{\frac{1}{n}\sum(y - \hat{y})^2}$ | < 10% |
| MAE | $\frac{1}{n}\sum|y - \hat{y}|$ | < 5% |
| Biais | $\frac{1}{n}\sum(y - \hat{y})$ | < 2% |

### 4.6.3 Limites méthodologiques

1. **Biais de sélection** : Utilisateurs de téléphonie ≠ population totale
2. **Biais géographique** : Couverture inégale du réseau
3. **Biais temporel** : Variations saisonnières non captées
4. **Biais de mesure** : Précision limitée de la localisation

---

*Méthodologie conforme au standard UN-MPDMS v2.0*  
*Date : Janvier 2026*
