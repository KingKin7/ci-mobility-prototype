# 1. Introduction

## Utilisation des données de téléphonie mobile dans la statistique officielle

---

## 1.1 Contexte général

### 1.1.1 La révolution des données mobiles

L'Afrique subsaharienne connaît une croissance exceptionnelle de la téléphonie mobile. En Côte d'Ivoire, le taux de pénétration mobile atteint **150%** en 2025, avec plus de **40 millions** d'abonnements actifs pour une population de 27 millions d'habitants. Cette ubiquité du téléphone portable génère quotidiennement des volumes massifs de données qui constituent une source d'information sans précédent sur les comportements et les mouvements de population.

### 1.1.2 Les limites des méthodes traditionnelles

Les systèmes statistiques nationaux reposent traditionnellement sur :

| Méthode | Fréquence | Coût | Délai | Couverture |
|---------|-----------|------|-------|------------|
| Recensement (RGPH) | 10 ans | Très élevé | 2-3 ans | Exhaustive |
| Enquêtes ménages | 3-5 ans | Élevé | 6-12 mois | Échantillon |
| Registres administratifs | Continue | Faible | Variable | Partielle |

Ces méthodes présentent des limitations majeures :
- **Coût prohibitif** des opérations de collecte sur le terrain
- **Délais importants** entre la collecte et la publication
- **Fréquence insuffisante** pour suivre des phénomènes dynamiques
- **Sous-couverture** des populations mobiles ou difficiles d'accès

### 1.1.3 L'opportunité des données CDR

Les **Call Detail Records (CDR)** offrent une alternative complémentaire avec des avantages significatifs :

| Caractéristique | Avantage |
|-----------------|----------|
| **Temporalité** | Données quasi temps réel |
| **Couverture** | Population mobile (>80% de la population) |
| **Coût marginal** | Données déjà collectées par les opérateurs |
| **Granularité** | Localisation au niveau des antennes (BTS) |
| **Continuité** | Flux continu de données |

---

## 1.2 Objectifs de l'étude

### 1.2.1 Objectif principal

> **Démontrer la faisabilité et la valeur ajoutée de l'utilisation des données de téléphonie mobile pour la production d'indicateurs statistiques officiels en Côte d'Ivoire.**

### 1.2.2 Objectifs spécifiques

1. **Développer des indicateurs de pauvreté**
   - Construire un indice de richesse basé sur les comportements téléphoniques
   - Calculer un Indice de Pauvreté Multidimensionnelle (IPM) adapté
   - Produire des cartes de pauvreté à haute résolution spatiale

2. **Mesurer les flux migratoires internes**
   - Détecter les changements de résidence à partir des traces de mobilité
   - Caractériser les corridors migratoires principaux
   - Identifier les schémas saisonniers de migration

3. **Analyser les patterns de mobilité quotidienne**
   - Cartographier les flux origine-destination
   - Identifier les heures de pointe et les zones de congestion
   - Segmenter la population selon les comportements de mobilité

4. **Établir un cadre méthodologique reproductible**
   - Documenter les méthodes conformément aux standards internationaux
   - Développer des outils open-source réutilisables
   - Proposer des recommandations pour l'intégration dans le système statistique national

### 1.2.3 Questions de recherche

| N° | Question | Indicateur cible |
|----|----------|------------------|
| Q1 | Les données CDR permettent-elles d'estimer la pauvreté ? | Corrélation avec enquêtes ménages |
| Q2 | Peut-on détecter les migrations internes ? | Taux de détection vs RGPH |
| Q3 | Quelle est la fiabilité des patterns de mobilité ? | Validation par enquêtes transport |
| Q4 | Les résultats sont-ils représentatifs ? | Comparaison avec données officielles |

---

## 1.3 Cadre institutionnel

### 1.3.1 L'Agence Nationale de la Statistique (ANStat)

L'ANStat est l'organe central du système statistique ivoirien, créé par la loi n°2013-537 du 30 juillet 2013. Ses missions incluent :

- La collecte, le traitement et la diffusion des statistiques officielles
- La coordination du système statistique national
- L'innovation méthodologique et technologique
- La formation et le renforcement des capacités

### 1.3.2 Le DataLab ANStat

Le DataLab est une unité d'innovation créée au sein de l'ANStat pour :

- Explorer les sources de données alternatives (Big Data)
- Développer des méthodes d'analyse avancées
- Prototyper des solutions avant industrialisation
- Former les statisticiens aux nouvelles technologies

### 1.3.3 Partenariats

| Partenaire | Rôle |
|------------|------|
| **UNFPA** | Appui technique et financier |
| **Banque Mondiale** | Méthodologie pauvreté |
| **OIM** | Standards migration |
| **Opérateurs télécoms** | Accès aux données (futur) |

---

## 1.4 Standards internationaux

### 1.4.1 UN-MPDMS (Mobile Positioning Data for Migration Statistics)

Ce projet s'appuie sur le standard **UN-MPDMS version 2.0** développé par la Division Statistique des Nations Unies. Ce cadre fournit :

- **Définitions harmonisées** des concepts de migration
- **Méthodes recommandées** pour la détection des changements de résidence
- **Indicateurs standardisés** pour la comparabilité internationale
- **Bonnes pratiques** en matière de protection des données

### 1.4.2 Principes fondamentaux

Le projet respecte les **Principes fondamentaux de la statistique officielle** des Nations Unies :

1. **Pertinence** : Répondre aux besoins des utilisateurs
2. **Impartialité** : Indépendance vis-à-vis des intérêts politiques
3. **Accessibilité** : Diffusion large des résultats
4. **Confidentialité** : Protection des données individuelles
5. **Qualité** : Méthodes rigoureuses et transparentes

### 1.4.3 RGPD et protection des données

Bien que la Côte d'Ivoire ne soit pas soumise au RGPD européen, le projet applique des principes équivalents :

| Principe | Application |
|----------|-------------|
| **Minimisation** | Seules les données nécessaires sont utilisées |
| **Anonymisation** | Aucune donnée nominative n'est conservée |
| **Agrégation** | Résultats publiés à un niveau agrégé (k-anonymat ≥ 5) |
| **Sécurité** | Accès restreint et données chiffrées |
| **Durée limitée** | Conservation limitée dans le temps |

---

## 1.5 Données synthétiques : justification

### 1.5.1 Pourquoi des données synthétiques ?

Ce prototype utilise des **données synthétiques** plutôt que des données réelles pour plusieurs raisons :

| Raison | Explication |
|--------|-------------|
| **Accès** | Accords avec opérateurs en cours de négociation |
| **Confidentialité** | Éviter tout risque de ré-identification |
| **Reproductibilité** | Permettre la réplication des analyses |
| **Démonstration** | Valider les méthodes avant accès aux vraies données |

### 1.5.2 Caractéristiques des données générées

Les données synthétiques sont générées pour :

- **Respecter les distributions réelles** (RGPH 2021, enquêtes ménages)
- **Reproduire les corrélations connues** entre variables
- **Simuler des patterns réalistes** de mobilité et migration
- **Couvrir l'ensemble du territoire** ivoirien

### 1.5.3 Limites

| Limite | Impact | Mitigation |
|--------|--------|------------|
| Pas de vraies traces CDR | Patterns simplifiés | Calibration sur études existantes |
| Corrélations artificielles | Risque de biais | Validation par experts |
| Volumes réduits | Précision limitée | Test de sensibilité |

---

## 1.6 Structure du document

Cette documentation est organisée en **8 chapitres** :

| Chapitre | Contenu |
|----------|---------|
| **1. Introduction** | Contexte, objectifs, cadre institutionnel |
| **2. Zone d'étude** | Géographie et démographie de la Côte d'Ivoire |
| **3. Description des données** | Dictionnaire des données et sources |
| **4. Méthodologie** | Méthodes de calcul et justifications |
| **5. Analyse descriptive** | Statistiques et visualisations |
| **6. Résultats** | Indicateurs calculés et cartes |
| **7. Interprétation** | Analyse et implications |
| **8. Conclusion** | Synthèse et recommandations |

Les **annexes** complètent le document avec :
- **Glossaire** des termes techniques
- **Références** bibliographiques
- **Exemples de code** Python

---

## 1.7 Public cible

Cette documentation s'adresse à plusieurs audiences :

| Audience | Intérêt principal |
|----------|-------------------|
| **Statisticiens ANStat** | Méthodes et reproductibilité |
| **Décideurs politiques** | Résultats et recommandations |
| **Chercheurs** | Méthodologie et validation |
| **Opérateurs télécoms** | Spécifications des données |
| **Bailleurs de fonds** | Impact et faisabilité |

---

**Document** : Introduction  
**Version** : 1.0  
**Date** : Janvier 2026  
**Projet** : CI-Mobility-Prototype  
**Standard** : UN-MPDMS v2.0