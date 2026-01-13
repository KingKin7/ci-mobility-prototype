# 7. Interprétation des Résultats

## 7.1 Introduction

Ce chapitre propose une interprétation approfondie des résultats obtenus, en les replaçant dans le contexte socio-économique de la Côte d'Ivoire et en examinant leurs implications pour les politiques publiques et la statistique officielle.

---

## 7.2 Interprétation des Indicateurs de Pauvreté

### 7.2.1 Validité de l'indice de richesse CDR

**Performance de l'ACP :**

La première composante principale explique **57.7%** de la variance totale, ce qui est considéré comme un excellent résultat pour un indice composite. Cette performance se compare favorablement aux indices de richesse traditionnels basés sur les actifs des ménages (DHS Wealth Index), qui expliquent généralement entre 40% et 60% de la variance.

**Structure de l'indice :**

L'analyse des loadings révèle une structure cohérente :

| Variable | Loading | Interprétation économique |
|----------|---------|---------------------------|
| Recharge (0.52) | Fort | Pouvoir d'achat direct |
| Data (0.48) | Fort | Accès aux services numériques |
| Appels (0.42) | Modéré | Capital social actif |
| Contacts (0.35) | Modéré | Réseau social |
| Mobilité (0.31) | Modéré | Accès aux opportunités |

Cette structure suggère que l'indice capture à la fois :
- **La dimension économique** (recharge, data)
- **La dimension sociale** (contacts, appels)
- **La dimension spatiale** (mobilité)

### 7.2.2 Signification de l'IPM à 0.206

L'Indice de Pauvreté Multidimensionnelle de **0.206** signifie que :
- **42.3%** de la population est considérée comme pauvre (incidence H)
- Ces pauvres souffrent en moyenne de **48.7%** des privations possibles (intensité A)

**Comparaison internationale :**

| Pays | IPM | Incidence (H) | Intensité (A) |
|------|-----|---------------|---------------|
| **Côte d'Ivoire (notre étude)** | **0.206** | **42.3%** | **48.7%** |
| Côte d'Ivoire (OPHI 2021) | 0.236 | 46.1% | 51.2% |
| Ghana (OPHI 2021) | 0.138 | 30.1% | 45.8% |
| Burkina Faso (OPHI 2021) | 0.523 | 83.8% | 62.4% |
| Sénégal (OPHI 2021) | 0.263 | 53.2% | 49.4% |

Notre estimation est légèrement inférieure à l'estimation OPHI officielle, ce qui peut s'expliquer par :
1. La surreprésentation des zones urbaines dans notre échantillon
2. Le biais de sélection (propriétaires de téléphones)
3. La période d'étude plus récente (amélioration tendancielle)

### 7.2.3 Le gradient Nord-Sud

La carte de pauvreté révèle un **gradient Nord-Sud** marqué :

```
NORD (Savanes, Denguélé)     : Taux pauvreté > 50%
     │
     │  Diminution progressive
     │
CENTRE (Bouaké, Yamoussoukro) : Taux pauvreté 35-45%
     │
     │  Diminution continue
     │
SUD (Abidjan, San-Pédro)      : Taux pauvreté < 30%
```

**Facteurs explicatifs :**

1. **Historiques** : Développement économique concentré au Sud depuis la colonisation
2. **Géographiques** : Accès aux ports, pluviométrie favorable au Sud
3. **Économiques** : Industries, services et commerce concentrés à Abidjan
4. **Infrastructurels** : Meilleure couverture réseau et routes au Sud

### 7.2.4 L'écart urbain/rural

L'écart de **17.4 points** entre les taux de pauvreté urbain (32.4%) et rural (49.8%) reflète :

- **L'accès différentiel aux services** : Éducation, santé, emplois formels
- **La densité d'opportunités** : Marchés, commerce, économie informelle dynamique
- **L'effet d'agglomération** : Économies d'échelle en milieu urbain

Cet écart est cohérent avec les observations de l'ENV 2018 (écart de 15-20 pp).

---

## 7.3 Interprétation des Flux Migratoires

### 7.3.1 Abidjan comme "métropole aspirante"

Le solde migratoire d'Abidjan (+225) représente **45%** des migrations totales, confirmant le rôle de la capitale économique comme principal pôle d'attraction du pays.

**Modèle gravitaire :**

Les flux migratoires suivent approximativement un modèle gravitaire :

$$F_{ij} = k \times \frac{P_i \times P_j}{d_{ij}^2}$$

Où :
- F_ij : flux de i vers j
- P : population
- d : distance
- k : constante

Les résidus par rapport à ce modèle révèlent :
- **Attractivité supérieure** : Abidjan, San-Pédro (économie portuaire)
- **Attractivité inférieure** : Régions du Nord (conflit passé, enclavement)

### 7.3.2 Profil du migrant type

L'analyse des caractéristiques des migrants révèle un profil cohérent avec la théorie économique de la migration (modèle de Harris-Todaro) :

| Caractéristique | Valeur | Implication |
|-----------------|--------|-------------|
| Âge moyen : 28.5 ans | Jeune adulte | Migration d'insertion professionnelle |
| 58% masculin | Surreprésentation hommes | Migration de travail |
| Indice richesse : +0.15 | Légèrement supérieur | Capacité à migrer |
| 42% origine urbaine | Minorité rurale | Migration en chaîne |

Ce profil suggère une **migration économique rationnelle** où les individus les plus aptes à bénéficier des opportunités urbaines sont ceux qui migrent.

### 7.3.3 Saisonnalité et calendrier

La saisonnalité des migrations reflète l'interaction entre plusieurs calendriers :

1. **Calendrier agricole** :
   - Creux en mai-juin (semis)
   - Creux en octobre-novembre (récoltes)

2. **Calendrier scolaire** :
   - Pic en juillet-août (vacances)
   - Migration des étudiants

3. **Calendrier social** :
   - Pic en décembre-janvier (fêtes, retours)
   - Migrations familiales

### 7.3.4 Implications pour le développement régional

Les déséquilibres migratoires observés ont des implications majeures :

**Pour les régions d'émigration (Nord) :**
- Perte de capital humain jeune et qualifié
- Vieillissement de la population
- Dépendance aux transferts de fonds
- Risque de "trappe à pauvreté"

**Pour Abidjan (immigration) :**
- Pression sur les services publics
- Étalement urbain et bidonvilles
- Dynamisme économique
- Défis de gouvernance urbaine

---

## 7.4 Interprétation de la Mobilité Quotidienne

### 7.4.1 Prédominance des transports informels

La structure modale observée (73% modes informels) reflète :

1. **L'insuffisance de l'offre formelle** :
   - SOTRA : 215 trajets soit 1.3% seulement
   - Couverture limitée aux axes principaux

2. **L'adaptation du secteur informel** :
   - Gbaka : desserte fine, fréquence élevée
   - Woro-woro : flexibilité, accessibilité tarifaire
   - Moto : rapidité, desserte des zones enclavées

3. **Les contraintes économiques** :
   - Marche : 31% des trajets, mode "par défaut" des plus pauvres

### 7.4.2 Congestion et perte d'efficacité

L'indice de congestion de **2.08** aux heures de pointe signifie que les trajets prennent en moyenne **deux fois plus de temps** qu'en conditions fluides.

**Coût économique estimé :**

| Élément | Calcul | Valeur |
|---------|--------|--------|
| Temps perdu moyen | 8.5 min × 16.9 trajets | 143.6 min/an/personne |
| Valeur du temps | 2 500 FCFA/heure | - |
| Coût individuel | 143.6/60 × 2 500 | 5 983 FCFA/an |
| Coût total (10 000 pers.) | 5 983 × 10 000 | **59.8 M FCFA/an** |

Extrapolé à l'échelle d'Abidjan (5 millions d'habitants),// filepath: d:\ci-mobility-prototype\docs\07_interpretation.md
# 7. Interprétation des Résultats

## 7.1 Introduction

Ce chapitre propose une interprétation approfondie des résultats obtenus, en les replaçant dans le contexte socio-économique de la Côte d'Ivoire et en examinant leurs implications pour les politiques publiques et la statistique officielle.

---

## 7.2 Interprétation des Indicateurs de Pauvreté

### 7.2.1 Validité de l'indice de richesse CDR

**Performance de l'ACP :**

La première composante principale explique **57.7%** de la variance totale, ce qui est considéré comme un excellent résultat pour un indice composite. Cette performance se compare favorablement aux indices de richesse traditionnels basés sur les actifs des ménages (DHS Wealth Index), qui expliquent généralement entre 40% et 60% de la variance.

**Structure de l'indice :**

L'analyse des loadings révèle une structure cohérente :

| Variable | Loading | Interprétation économique |
|----------|---------|---------------------------|
| Recharge (0.52) | Fort | Pouvoir d'achat direct |
| Data (0.48) | Fort | Accès aux services numériques |
| Appels (0.42) | Modéré | Capital social actif |
| Contacts (0.35) | Modéré | Réseau social |
| Mobilité (0.31) | Modéré | Accès aux opportunités |

Cette structure suggère que l'indice capture à la fois :
- **La dimension économique** (recharge, data)
- **La dimension sociale** (contacts, appels)
- **La dimension spatiale** (mobilité)

### 7.2.2 Signification de l'IPM à 0.206

L'Indice de Pauvreté Multidimensionnelle de **0.206** signifie que :
- **42.3%** de la population est considérée comme pauvre (incidence H)
- Ces pauvres souffrent en moyenne de **48.7%** des privations possibles (intensité A)

**Comparaison internationale :**

| Pays | IPM | Incidence (H) | Intensité (A) |
|------|-----|---------------|---------------|
| **Côte d'Ivoire (notre étude)** | **0.206** | **42.3%** | **48.7%** |
| Côte d'Ivoire (OPHI 2021) | 0.236 | 46.1% | 51.2% |
| Ghana (OPHI 2021) | 0.138 | 30.1% | 45.8% |
| Burkina Faso (OPHI 2021) | 0.523 | 83.8% | 62.4% |
| Sénégal (OPHI 2021) | 0.263 | 53.2% | 49.4% |

Notre estimation est légèrement inférieure à l'estimation OPHI officielle, ce qui peut s'expliquer par :
1. La surreprésentation des zones urbaines dans notre échantillon
2. Le biais de sélection (propriétaires de téléphones)
3. La période d'étude plus récente (amélioration tendancielle)

### 7.2.3 Le gradient Nord-Sud

La carte de pauvreté révèle un **gradient Nord-Sud** marqué :

```
NORD (Savanes, Denguélé)     : Taux pauvreté > 50%
     │
     │  Diminution progressive
     │
CENTRE (Bouaké, Yamoussoukro) : Taux pauvreté 35-45%
     │
     │  Diminution continue
     │
SUD (Abidjan, San-Pédro)      : Taux pauvreté < 30%
```

**Facteurs explicatifs :**

1. **Historiques** : Développement économique concentré au Sud depuis la colonisation
2. **Géographiques** : Accès aux ports, pluviométrie favorable au Sud
3. **Économiques** : Industries, services et commerce concentrés à Abidjan
4. **Infrastructurels** : Meilleure couverture réseau et routes au Sud

### 7.2.4 L'écart urbain/rural

L'écart de **17.4 points** entre les taux de pauvreté urbain (32.4%) et rural (49.8%) reflète :

- **L'accès différentiel aux services** : Éducation, santé, emplois formels
- **La densité d'opportunités** : Marchés, commerce, économie informelle dynamique
- **L'effet d'agglomération** : Économies d'échelle en milieu urbain

Cet écart est cohérent avec les observations de l'ENV 2018 (écart de 15-20 pp).

---

## 7.3 Interprétation des Flux Migratoires

### 7.3.1 Abidjan comme "métropole aspirante"

Le solde migratoire d'Abidjan (+225) représente **45%** des migrations totales, confirmant le rôle de la capitale économique comme principal pôle d'attraction du pays.

**Modèle gravitaire :**

Les flux migratoires suivent approximativement un modèle gravitaire :

$$F_{ij} = k \times \frac{P_i \times P_j}{d_{ij}^2}$$

Où :
- F_ij : flux de i vers j
- P : population
- d : distance
- k : constante

Les résidus par rapport à ce modèle révèlent :
- **Attractivité supérieure** : Abidjan, San-Pédro (économie portuaire)
- **Attractivité inférieure** : Régions du Nord (conflit passé, enclavement)

### 7.3.2 Profil du migrant type

L'analyse des caractéristiques des migrants révèle un profil cohérent avec la théorie économique de la migration (modèle de Harris-Todaro) :

| Caractéristique | Valeur | Implication |
|-----------------|--------|-------------|
| Âge moyen : 28.5 ans | Jeune adulte | Migration d'insertion professionnelle |
| 58% masculin | Surreprésentation hommes | Migration de travail |
| Indice richesse : +0.15 | Légèrement supérieur | Capacité à migrer |
| 42% origine urbaine | Minorité rurale | Migration en chaîne |

Ce profil suggère une **migration économique rationnelle** où les individus les plus aptes à bénéficier des opportunités urbaines sont ceux qui migrent.

### 7.3.3 Saisonnalité et calendrier

La saisonnalité des migrations reflète l'interaction entre plusieurs calendriers :

1. **Calendrier agricole** :
   - Creux en mai-juin (semis)
   - Creux en octobre-novembre (récoltes)

2. **Calendrier scolaire** :
   - Pic en juillet-août (vacances)
   - Migration des étudiants

3. **Calendrier social** :
   - Pic en décembre-janvier (fêtes, retours)
   - Migrations familiales

### 7.3.4 Implications pour le développement régional

Les déséquilibres migratoires observés ont des implications majeures :

**Pour les régions d'émigration (Nord) :**
- Perte de capital humain jeune et qualifié
- Vieillissement de la population
- Dépendance aux transferts de fonds
- Risque de "trappe à pauvreté"

**Pour Abidjan (immigration) :**
- Pression sur les services publics
- Étalement urbain et bidonvilles
- Dynamisme économique
- Défis de gouvernance urbaine

---

## 7.4 Interprétation de la Mobilité Quotidienne

### 7.4.1 Prédominance des transports informels

La structure modale observée (73% modes informels) reflète :

1. **L'insuffisance de l'offre formelle** :
   - SOTRA : 215 trajets soit 1.3% seulement
   - Couverture limitée aux axes principaux

2. **L'adaptation du secteur informel** :
   - Gbaka : desserte fine, fréquence élevée
   - Woro-woro : flexibilité, accessibilité tarifaire
   - Moto : rapidité, desserte des zones enclavées

3. **Les contraintes économiques** :
   - Marche : 31% des trajets, mode "par défaut" des plus pauvres

### 7.4.2 Congestion et perte d'efficacité

L'indice de congestion de **2.08** aux heures de pointe signifie que les trajets prennent en moyenne **deux fois plus de temps** qu'en conditions fluides.

**Coût économique estimé :**

| Élément | Calcul | Valeur |
|---------|--------|--------|
| Temps perdu moyen | 8.5 min × 16.9 trajets | 143.6 min/an/personne |
| Valeur du temps | 2 500 FCFA/heure | - |
| Coût individuel | 143.6/60 × 2 500 | 5 983 FCFA/an |
| Coût total (10 000 pers.) | 5 983 × 10 000 | **59.8 M FCFA/an** |

Extrapolé à l'échelle d'Abidjan (5 millions d'habitants),