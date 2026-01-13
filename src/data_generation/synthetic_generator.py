"""
Générateur de données synthétiques conformes aux standards UN
Projet: Mobilité Côte d'Ivoire - ANStat
Version: 1.1.0

Ce module génère des données fictives de téléphonie mobile pour:
- L'analyse de la pauvreté
- L'analyse de la migration
- L'analyse de la mobilité quotidienne

MISE À JOUR v1.1:
- Compatible h3 v4.x (nouvelle API)
- Intégration des limites GADM Côte d'Ivoire
"""

import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import geopandas as gpd
import numpy as np
import pandas as pd
import yaml
from loguru import logger
from shapely.geometry import Point

# Configuration du logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logger.add(
    "logs/generator_{time}.log", rotation="1 day", retention="7 days", level="INFO"
)


class SyntheticDataGenerator:
    """
    Générateur de données synthétiques conformes UN-MPDMS/MPDMIS

    Cette classe génère des données fictives réalistes pour tester
    le pipeline d'analyse de données de téléphonie mobile.
    """

    def __init__(self, config_path: str = "config/data_params.yml"):
        """
        Initialise le générateur avec la configuration

        Args:
            config_path: Chemin vers le fichier de configuration YAML
        """
        self.config_path = Path(config_path)
        self._load_config()
        self._setup_random_state()
        self._load_gadm_boundaries()

        logger.info(f"Générateur initialisé avec {self.n_users} utilisateurs")

    def _load_config(self) -> None:
        """Charge la configuration depuis le fichier YAML"""
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        # Extraction des paramètres principaux
        self.n_users = self.config["generation"]["n_users"]
        self.start_date = pd.to_datetime(self.config["generation"]["start_date"])
        self.end_date = pd.to_datetime(self.config["generation"]["end_date"])
        self.days = self.config["generation"]["days_to_generate"]
        self.seed = self.config["generation"]["random_seed"]

        # Paramètres spatiaux
        self.spatial_bounds = self.config["spatial_bounds"]
        self.urban_centers = self.config["urban_centers"]

        # Distributions démographiques
        self.demographics = self.config["demographics"]

        # Paramètres de mobilité
        self.mobility_config = self.config["mobility"]

        # Paramètres économiques
        self.economic_config = self.config["economic"]

        # Paramètres de migration
        self.migration_config = self.config["migration"]

    def _setup_random_state(self) -> None:
        """Configure le générateur aléatoire pour reproductibilité"""
        np.random.seed(self.seed)
        self.rng = np.random.default_rng(self.seed)

    def _load_gadm_boundaries(self) -> None:
        """Charge les limites administratives GADM si disponibles"""
        gadm_path = Path("data/raw/gadm41_CIV_4.json")

        if gadm_path.exists():
            logger.info(f"Chargement des limites GADM depuis {gadm_path}")
            self.gadm = gpd.read_file(gadm_path)
            self.has_gadm = True

            # Créer un mapping des localités avec leurs centroïdes et poids
            self._prepare_localities()
            logger.info(f"✓ {len(self.gadm)} localités GADM chargées")
        else:
            logger.warning(f"Fichier GADM non trouvé: {gadm_path}")
            self.has_gadm = False
            self.gadm = None

    def _prepare_localities(self) -> None:
        """Prépare les localités avec centroïdes et poids de population"""
        # Calculer les centroïdes
        self.gadm["centroid"] = self.gadm.geometry.centroid
        self.gadm["centroid_lat"] = self.gadm["centroid"].y
        self.gadm["centroid_lon"] = self.gadm["centroid"].x

        # Définir les poids de population (approximatifs)
        # Les grandes villes ont plus de poids
        major_cities = {
            "Abidjan-Ville": 0.35,
            "Bouake": 0.10,
            "Yamoussoukro": 0.05,
            "Korhogo": 0.04,
            "San-Pedro": 0.04,
            "Daloa": 0.03,
            "Man": 0.03,
            "Gagnoa": 0.02,
            "Divo": 0.02,
            "Abengourou": 0.02,
        }

        # Poids par défaut pour les autres localités
        remaining_weight = 1.0 - sum(major_cities.values())
        n_other = len(self.gadm) - len(major_cities)
        default_weight = remaining_weight / n_other if n_other > 0 else 0.01

        self.gadm["weight"] = (
            self.gadm["NAME_4"].map(major_cities).fillna(default_weight)
        )

        # Normaliser les poids
        self.gadm["weight"] = self.gadm["weight"] / self.gadm["weight"].sum()

        # Liste des localités pour sélection aléatoire
        self.localities = self.gadm["NAME_4"].tolist()
        self.locality_weights = self.gadm["weight"].tolist()

    def _generate_user_id(self, index: int) -> str:
        """
        Génère un identifiant anonymisé pour un utilisateur

        Args:
            index: Index de l'utilisateur

        Returns:
            Hash SHA-256 tronqué
        """
        salt = datetime.now().isoformat()
        raw_id = f"user_{index}_{salt}"
        return hashlib.sha256(raw_id.encode()).hexdigest()[:12]

    def _get_random_point_in_locality(self, locality_name: str) -> Tuple[float, float]:
        """
        Génère un point aléatoire dans une localité GADM

        Args:
            locality_name: Nom de la localité (NAME_4)

        Returns:
            Tuple (latitude, longitude)
        """
        locality = self.gadm[self.gadm["NAME_4"] == locality_name].iloc[0]
        geometry = locality.geometry

        # Générer un point aléatoire dans le polygone
        minx, miny, maxx, maxy = geometry.bounds

        max_attempts = 100
        for _ in range(max_attempts):
            random_point = Point(
                self.rng.uniform(minx, maxx), self.rng.uniform(miny, maxy)
            )
            if geometry.contains(random_point):
                return random_point.y, random_point.x  # lat, lon

        # Fallback: utiliser le centroïde avec bruit
        centroid = geometry.centroid
        lat = centroid.y + self.rng.normal(0, 0.02)
        lon = centroid.x + self.rng.normal(0, 0.02)
        return lat, lon

    def _assign_home_location(self) -> Tuple[str, float, float, str, str]:
        """
        Attribue une localisation de résidence basée sur GADM ou config

        Returns:
            Tuple (locality_name, latitude, longitude, region, department)
        """
        if self.has_gadm:
            # Sélectionner une localité selon les poids
            locality_name = self.rng.choice(self.localities, p=self.locality_weights)
            lat, lon = self._get_random_point_in_locality(locality_name)

            # Récupérer les infos administratives
            locality_data = self.gadm[self.gadm["NAME_4"] == locality_name].iloc[0]
            region = locality_data["NAME_1"]
            department = locality_data["NAME_2"]

            return locality_name, lat, lon, region, department
        else:
            # Fallback sur la config originale
            cities = list(self.urban_centers.keys())
            weights = [self.urban_centers[c]["weight"] for c in cities]

            city = self.rng.choice(cities, p=weights)

            if city != "Others":
                base_lat = self.urban_centers[city]["lat"]
                base_lon = self.urban_centers[city]["lon"]
                lat = base_lat + self.rng.normal(0, 0.05)
                lon = base_lon + self.rng.normal(0, 0.05)
            else:
                lat = self.rng.uniform(4.5, 10.0)
                lon = self.rng.uniform(-8.0, -3.0)

            return city, lat, lon, "Unknown", "Unknown"

    def _get_h3_cell(self, lat: float, lon: float, resolution: int = 7) -> str:
        """
        Calcule la cellule H3 pour une position
        Compatible avec h3 v4.x

        Args:
            lat: Latitude
            lon: Longitude
            resolution: Résolution H3 (défaut: 7, ~1.41km)

        Returns:
            Index H3 de la cellule
        """
        try:
            import h3

            # h3 v4.x utilise latlng_to_cell au lieu de geo_to_h3
            if hasattr(h3, "latlng_to_cell"):
                # h3 v4.x
                return h3.latlng_to_cell(lat, lon, resolution)
            elif hasattr(h3, "geo_to_h3"):
                # h3 v3.x (ancienne API)
                return h3.geo_to_h3(lat, lon, resolution)
            else:
                raise AttributeError("API h3 non reconnue")
        except Exception as e:
            # Fallback si h3 pose problème
            logger.warning(f"Erreur h3: {e}, utilisation du fallback")
            return f"h3_{int(lat*1000)}_{int(abs(lon)*1000)}_{resolution}"

    def generate_user_profiles(self) -> pd.DataFrame:
        """
        Génère les profils utilisateurs avec caractéristiques socio-démographiques

        Returns:
            DataFrame avec les profils utilisateurs
        """
        logger.info(f"Génération de {self.n_users} profils utilisateurs...")

        users = []

        for i in range(self.n_users):
            # Localisation de base (avec GADM si disponible)
            locality, home_lat, home_lon, region, department = (
                self._assign_home_location()
            )

            # Cellule H3 de résidence
            home_h3 = self._get_h3_cell(home_lat, home_lon)

            # Caractéristiques démographiques
            demo = self.demographics

            age_group = self.rng.choice(
                demo["age_groups"]["values"], p=demo["age_groups"]["probabilities"]
            )

            gender = self.rng.choice(
                demo["gender"]["values"], p=demo["gender"]["probabilities"]
            )

            occupation = self.rng.choice(
                demo["occupation"]["values"], p=demo["occupation"]["probabilities"]
            )

            phone_type = self.rng.choice(
                demo["phone_type"]["values"], p=demo["phone_type"]["probabilities"]
            )

            subscription = self.rng.choice(
                demo["subscription"]["values"], p=demo["subscription"]["probabilities"]
            )

            # Zone urbaine/rurale basée sur la localité
            urban_localities = [
                "Abidjan-Ville",
                "Bouake",
                "Yamoussoukro",
                "Korhogo",
                "San-Pedro",
                "Daloa",
                "Man",
                "Gagnoa",
                "Divo",
                "Abengourou",
                "Anyama",
                "Bingerville",
                "Grand-Bassam",
                "Aboisso",
            ]

            if locality in urban_localities:
                urban_rural = "urban"
            else:
                urban_rural = self.rng.choice(["urban", "rural"], p=[0.3, 0.7])

            # Taille du ménage
            household_size = self.rng.choice(
                range(1, 9), p=[0.05, 0.15, 0.20, 0.25, 0.15, 0.10, 0.07, 0.03]
            )

            # Score de richesse initial
            wealth_score = self._estimate_initial_wealth(
                phone_type, subscription, occupation, urban_rural
            )

            users.append(
                {
                    "user_id": self._generate_user_id(i),
                    "age_group": age_group,
                    "gender": gender,
                    "occupation": occupation,
                    "phone_type": phone_type,
                    "subscription_type": subscription,
                    "home_lat": round(home_lat, 6),
                    "home_lon": round(home_lon, 6),
                    "home_h3": home_h3,
                    "locality": locality,
                    "department": department,
                    "region": region,
                    "urban_rural": urban_rural,
                    "household_size": household_size,
                    "initial_wealth_score": round(wealth_score, 3),
                    "creation_timestamp": datetime.now().isoformat(),
                }
            )

            # Log de progression
            if (i + 1) % 1000 == 0:
                logger.info(f"  {i + 1}/{self.n_users} profils générés...")

        df = pd.DataFrame(users)
        logger.info(f"✓ {len(df)} profils utilisateurs générés")

        return df

    def _estimate_initial_wealth(
        self, phone_type: str, subscription: str, occupation: str, urban_rural: str
    ) -> float:
        """
        Estime un score de richesse initial basé sur les caractéristiques

        Returns:
            Score entre 0 et 1
        """
        score = 0.5  # Base

        # Type de téléphone
        phone_scores = {"basic": -0.2, "feature": 0.0, "smartphone": 0.2}
        score += phone_scores.get(phone_type, 0)

        # Type d'abonnement
        if subscription == "postpaid":
            score += 0.15

        # Occupation
        occupation_scores = {
            "employee": 0.15,
            "trader": 0.1,
            "student": 0.0,
            "informal_sector": -0.1,
            "farmer": -0.1,
            "unemployed": -0.2,
            "other": 0.0,
        }
        score += occupation_scores.get(occupation, 0)

        # Zone
        if urban_rural == "urban":
            score += 0.05
        else:
            score -= 0.05

        # Normalisation et bruit
        score = max(0, min(1, score + self.rng.normal(0, 0.1)))

        return score

    def generate_poverty_data(self, users_df: pd.DataFrame) -> pd.DataFrame:
        """
        Génère les données spécifiques à l'analyse de la pauvreté

        Args:
            users_df: DataFrame des profils utilisateurs

        Returns:
            DataFrame avec les indicateurs de pauvreté
        """
        logger.info("Génération des données de pauvreté...")

        poverty_records = []

        for idx, user in users_df.iterrows():
            wealth = user["initial_wealth_score"]

            # Sélection des probabilités de recharge selon le niveau de richesse
            if wealth < 0.4:
                recharge_probs = self.economic_config["recharge_probs_poor"]
            else:
                recharge_probs = self.economic_config["recharge_probs_rich"]

            # Génération des patterns de recharge sur la période
            for day_offset in range(0, self.days, 7):  # Données hebdomadaires
                current_date = self.start_date + timedelta(days=day_offset)

                # Nombre de recharges dans la semaine
                n_recharges = self.rng.poisson(max(1, wealth * 5 + 2))

                # Montant total des recharges
                amounts = self.rng.choice(
                    self.economic_config["recharge_amounts"],
                    size=n_recharges,
                    p=recharge_probs,
                )
                total_recharge = int(amounts.sum())

                # Durée d'appel (corrélée à la richesse)
                call_duration = int(self.rng.gamma(shape=2 + wealth * 3, scale=60))

                # Volume de données (corrélé au type de téléphone et richesse)
                if user["phone_type"] == "smartphone":
                    data_mb = round(self.rng.gamma(20 + wealth * 50, 10), 1)
                elif user["phone_type"] == "feature":
                    data_mb = round(self.rng.gamma(5 + wealth * 20, 5), 1)
                else:
                    data_mb = round(self.rng.exponential(2), 1)

                # Score de diversité des contacts
                contact_diversity = round(
                    min(1, max(0, 0.3 + wealth * 0.4 + self.rng.normal(0, 0.15))), 2
                )

                # Rayon de mobilité (corrélé à la richesse)
                mobility_radius = round(max(0.1, self.rng.gamma(1 + wealth * 5, 2)), 1)

                poverty_records.append(
                    {
                        "user_id": user["user_id"],
                        "timestamp": current_date.isoformat(),
                        "week_start": current_date.strftime("%Y-%m-%d"),
                        "latitude": user["home_lat"],
                        "longitude": user["home_lon"],
                        "locality": user["locality"],
                        "department": user.get("department", "Unknown"),
                        "region": user.get("region", "Unknown"),
                        "antenna_id": f"ANT_{self.rng.integers(100, 999)}",
                        "call_duration_sec": call_duration,
                        "data_mb": data_mb,
                        "recharge_amount_fcfa": total_recharge,
                        "recharge_frequency_weekly": n_recharges,
                        "contact_diversity_score": contact_diversity,
                        "mobility_radius_km": mobility_radius,
                        "phone_type": user["phone_type"],
                        "subscription_type": user["subscription_type"],
                    }
                )

            # Log de progression
            if (idx + 1) % 2000 == 0:
                logger.info(f"  {idx + 1}/{len(users_df)} utilisateurs traités...")

        df = pd.DataFrame(poverty_records)
        logger.info(f"✓ {len(df)} enregistrements de pauvreté générés")

        return df

    def generate_migration_data(self, users_df: pd.DataFrame) -> pd.DataFrame:
        """
        Génère les données de migration interne

        Args:
            users_df: DataFrame des profils utilisateurs

        Returns:
            DataFrame avec les événements de migration
        """
        logger.info("Génération des données de migration...")

        migration_types = [
            "permanent_relocation",
            "work_migration",
            "education_migration",
            "seasonal_agriculture",
            "temporary_stay",
            "circular_migration",
        ]

        migration_probs = [0.15, 0.30, 0.10, 0.20, 0.15, 0.10]

        migration_records = []

        # Utiliser les localités GADM si disponibles
        if self.has_gadm:
            available_localities = self.localities
        else:
            available_localities = [
                c for c in self.urban_centers.keys() if c != "Others"
            ]

        # Sélectionner un sous-ensemble d'utilisateurs qui migrent
        n_migrants = int(self.n_users * self.migration_config["migration_probability"])
        migrant_indices = self.rng.choice(len(users_df), size=n_migrants, replace=False)

        for idx in migrant_indices:
            user = users_df.iloc[idx]

            # Origine
            origin_locality = user["locality"]
            origin_lat = user["home_lat"]
            origin_lon = user["home_lon"]

            # Destination (différente de l'origine)
            available_dests = [c for c in available_localities if c != origin_locality]
            if not available_dests:
                available_dests = available_localities

            dest_locality = self.rng.choice(available_dests)

            # Obtenir les coordonnées de destination
            if self.has_gadm:
                dest_lat, dest_lon = self._get_random_point_in_locality(dest_locality)
                dest_data = self.gadm[self.gadm["NAME_4"] == dest_locality].iloc[0]
                dest_region = dest_data["NAME_1"]
                dest_department = dest_data["NAME_2"]
            else:
                if dest_locality in self.urban_centers:
                    dest_lat = self.urban_centers[dest_locality][
                        "lat"
                    ] + self.rng.normal(0, 0.05)
                    dest_lon = self.urban_centers[dest_locality][
                        "lon"
                    ] + self.rng.normal(0, 0.05)
                else:
                    dest_lat = self.rng.uniform(5, 10)
                    dest_lon = self.rng.uniform(-8, -4)
                dest_region = "Unknown"
                dest_department = "Unknown"

            # Calcul de la distance
            distance_km = self._haversine_distance(
                origin_lat, origin_lon, dest_lat, dest_lon
            )

            # Type de migration
            migration_type = self.rng.choice(migration_types, p=migration_probs)

            # Durée de résidence
            if migration_type in ["permanent_relocation", "work_migration"]:
                residence_days = int(self.rng.uniform(90, 365))
            elif migration_type == "education_migration":
                residence_days = int(self.rng.uniform(120, 300))
            elif migration_type == "seasonal_agriculture":
                residence_days = int(self.rng.uniform(30, 120))
            else:
                residence_days = int(self.rng.uniform(7, 60))

            # Migration de retour?
            is_return = self.rng.random() < 0.3

            # Date de détection
            detection_date = self.start_date + timedelta(
                days=int(self.rng.integers(0, self.days))
            )

            # Historique des localisations
            previous_locations = [origin_locality]
            if is_return and len(available_localities) > 2:
                intermediate = self.rng.choice(
                    [
                        c
                        for c in available_localities
                        if c not in [origin_locality, dest_locality]
                    ][:3]
                )
                previous_locations.append(intermediate)

            migration_records.append(
                {
                    "user_id": user["user_id"],
                    "timestamp": detection_date.isoformat(),
                    "origin_locality": origin_locality,
                    "origin_region": user.get("region", "Unknown"),
                    "current_locality": dest_locality,
                    "current_region": dest_region,
                    "origin_lat": round(origin_lat, 6),
                    "origin_lon": round(origin_lon, 6),
                    "current_lat": round(dest_lat, 6),
                    "current_lon": round(dest_lon, 6),
                    "residence_duration_days": residence_days,
                    "movement_type": migration_type,
                    "is_return_migration": is_return,
                    "previous_locations": str(previous_locations),
                    "distance_km": round(distance_km, 1),
                }
            )

        df = pd.DataFrame(migration_records)
        logger.info(f"✓ {len(df)} événements de migration générés")

        return df

    def generate_mobility_data(self, users_df: pd.DataFrame) -> pd.DataFrame:
        """
        Génère les données de mobilité quotidienne (trajets)

        Args:
            users_df: DataFrame des profils utilisateurs

        Returns:
            DataFrame avec les trajets
        """
        logger.info("Génération des données de mobilité...")

        transport_modes = [
            "walking",
            "bicycle",
            "bus",
            "taxi",
            "motorbike",
            "personal_car",
        ]
        trip_purposes = [
            "home_to_work",
            "work_to_home",
            "work_internal",
            "shopping",
            "leisure",
            "health",
            "education",
            "other",
        ]

        mobility_records = []

        # Générer pour un échantillon d'utilisateurs (pour limiter la taille)
        sample_size = min(1000, self.n_users)
        sample_users = users_df.sample(n=sample_size, random_state=self.seed)

        logger.info(f"  Génération pour {sample_size} utilisateurs...")

        for idx, (_, user) in enumerate(sample_users.iterrows()):
            wealth = user["initial_wealth_score"]

            # Nombre de jours à générer pour cet utilisateur
            n_days = min(7, self.days)

            for day_offset in range(n_days):
                current_date = self.start_date + timedelta(days=day_offset)

                # Pas de déplacements le dimanche pour certains
                if current_date.weekday() == 6 and self.rng.random() < 0.4:
                    continue

                # Nombre de trajets dans la journée
                if user["occupation"] == "employee":
                    n_trips = self.rng.poisson(4)
                elif user["occupation"] == "student":
                    n_trips = self.rng.poisson(3)
                else:
                    n_trips = self.rng.poisson(2)

                for trip_num in range(max(1, n_trips)):
                    trip_id = f"TRIP_{user['user_id'][:6]}_{day_offset}_{trip_num}"

                    # Heure du trajet
                    if trip_num == 0:
                        hour = int(max(5, min(10, self.rng.normal(7, 1))))
                    elif trip_num == n_trips - 1:
                        hour = int(max(16, min(22, self.rng.normal(18, 2))))
                    else:
                        hour = int(self.rng.uniform(9, 17))

                    minute = self.rng.integers(0, 60)

                    # Origine (domicile ou position précédente)
                    origin_lat = user["home_lat"] + self.rng.normal(0, 0.02)
                    origin_lon = user["home_lon"] + self.rng.normal(0, 0.02)

                    # Distance et destination
                    mobility_radius = self.mobility_config["mobility_radius_mean"]
                    if wealth > 0.5:
                        mobility_radius *= 1.5

                    angle = self.rng.uniform(0, 2 * np.pi)
                    distance = abs(self.rng.exponential(mobility_radius / 3))

                    dest_lat = origin_lat + (distance / 111) * np.cos(angle)
                    dest_lon = origin_lon + (distance / 111) * np.sin(angle)

                    # Mode de transport basé sur la distance et la richesse
                    if distance < 1:
                        mode = "walking"
                        speed = self.rng.uniform(4, 6)
                    elif distance < 3:
                        if wealth > 0.6:
                            mode = self.rng.choice(
                                ["taxi", "motorbike", "personal_car"]
                            )
                        else:
                            mode = self.rng.choice(["walking", "bus", "motorbike"])
                        speed = self.rng.uniform(8, 20)
                    else:
                        if wealth > 0.7:
                            mode = self.rng.choice(["taxi", "personal_car"])
                            speed = self.rng.uniform(25, 50)
                        else:
                            mode = self.rng.choice(["bus", "taxi", "motorbike"])
                            speed = self.rng.uniform(15, 35)

                    # Durée du trajet
                    duration_min = int(max(1, (distance / speed) * 60))

                    # Motif du trajet
                    if trip_num == 0:
                        purpose = "home_to_work"
                    elif trip_num == n_trips - 1:
                        purpose = "work_to_home"
                    else:
                        purpose = self.rng.choice(
                            ["work_internal", "shopping", "leisure", "health", "other"]
                        )

                    mobility_records.append(
                        {
                            "user_id": user["user_id"],
                            "timestamp": f"{current_date.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}:00",
                            "trip_id": trip_id,
                            "origin_lat": round(origin_lat, 6),
                            "origin_lon": round(origin_lon, 6),
                            "dest_lat": round(dest_lat, 6),
                            "dest_lon": round(dest_lon, 6),
                            "origin_antenna": f"ANT_{self.rng.integers(100, 999)}",
                            "dest_antenna": f"ANT_{self.rng.integers(100, 999)}",
                            "duration_min": duration_min,
                            "distance_km": round(distance, 2),
                            "speed_kmh": round(speed, 1),
                            "transport_mode": mode,
                            "trip_purpose": purpose,
                            "hour_of_day": hour,
                            "locality": user["locality"],
                        }
                    )

            # Log de progression
            if (idx + 1) % 200 == 0:
                logger.info(f"  {idx + 1}/{sample_size} utilisateurs traités...")

        df = pd.DataFrame(mobility_records)
        logger.info(f"✓ {len(df)} trajets de mobilité générés")

        return df

    def _haversine_distance(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        Calcule la distance en km entre deux points GPS

        Returns:
            Distance en kilomètres
        """
        R = 6371  # Rayon de la Terre en km

        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))

        return R * c

    def save_datasets(
        self,
        users_df: pd.DataFrame,
        poverty_df: pd.DataFrame,
        migration_df: pd.DataFrame,
        mobility_df: pd.DataFrame,
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Sauvegarde tous les datasets générés
        """
        if output_dir is None:
            output_dir = self.config["paths"]["output_dir"]

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Timestamp pour versionning
        version = datetime.now().strftime("%Y%m%d_%H%M%S")

        saved_files = {}

        # Sauvegarde en CSV et Parquet
        datasets = {
            "users": users_df,
            "poverty": poverty_df,
            "migration": migration_df,
            "mobility": mobility_df,
        }

        for name, df in datasets.items():
            # CSV
            csv_path = output_path / f"{name}_{version}.csv"
            df.to_csv(csv_path, index=False)
            saved_files[f"{name}_csv"] = str(csv_path)

            # Parquet
            parquet_path = output_path / f"{name}_{version}.parquet"
            df.to_parquet(parquet_path, index=False, compression="snappy")
            saved_files[f"{name}_parquet"] = str(parquet_path)

            logger.info(f"  ✓ {name}: {len(df)} enregistrements sauvegardés")

        # Métadonnées
        metadata = {
            "version": version,
            "generation_timestamp": datetime.now().isoformat(),
            "config_used": str(self.config_path),
            "n_users": self.n_users,
            "gadm_used": self.has_gadm,
            "period": {
                "start": self.start_date.isoformat(),
                "end": self.end_date.isoformat(),
            },
            "datasets": {
                "users": {"rows": len(users_df), "columns": list(users_df.columns)},
                "poverty": {
                    "rows": len(poverty_df),
                    "columns": list(poverty_df.columns),
                },
                "migration": {
                    "rows": len(migration_df),
                    "columns": list(migration_df.columns),
                },
                "mobility": {
                    "rows": len(mobility_df),
                    "columns": list(mobility_df.columns),
                },
            },
        }

        metadata_path = output_path / f"metadata_{version}.yml"
        with open(metadata_path, "w", encoding="utf-8") as f:
            yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True)
        saved_files["metadata"] = str(metadata_path)

        logger.info(f"✓ Datasets sauvegardés dans {output_path}")

        return saved_files

    def generate_all(self, save: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Génère tous les datasets en une seule commande
        """
        logger.info("=== Démarrage de la génération complète ===")

        # 1. Profils utilisateurs
        users_df = self.generate_user_profiles()

        # 2. Données de pauvreté
        poverty_df = self.generate_poverty_data(users_df)

        # 3. Données de migration
        migration_df = self.generate_migration_data(users_df)

        # 4. Données de mobilité
        mobility_df = self.generate_mobility_data(users_df)

        # Sauvegarde si demandé
        if save:
            self.save_datasets(users_df, poverty_df, migration_df, mobility_df)

        logger.info("=== Génération complète terminée ===")

        return {
            "users": users_df,
            "poverty": poverty_df,
            "migration": migration_df,
            "mobility": mobility_df,
        }


def main():
    """Point d'entrée principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Génération de données synthétiques de téléphonie mobile"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/data_params.yml",
        help="Chemin vers le fichier de configuration",
    )
    parser.add_argument(
        "--output", type=str, default=None, help="Répertoire de sortie (optionnel)"
    )
    parser.add_argument(
        "--no-save", action="store_true", help="Ne pas sauvegarder les fichiers"
    )

    args = parser.parse_args()

    # Génération
    generator = SyntheticDataGenerator(config_path=args.config)
    datasets = generator.generate_all(save=not args.no_save)

    # Affichage du résumé
    print("\n=== Résumé de la génération ===")
    for name, df in datasets.items():
        print(f"  {name}: {len(df)} enregistrements, {len(df.columns)} colonnes")


if __name__ == "__main__":
    main()
