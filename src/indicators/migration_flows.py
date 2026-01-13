"""
Détecteur de migrations internes
Conforme aux standards UN-MPDMS (Mobile Positioning Data for Migration Statistics)

Ce module détecte et caractérise les migrations à partir
des changements de localisation résidentielle.
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from loguru import logger


class MigrationDetector:
    """
    Détecte les migrations à partir des données de localisation

    Méthodologie UN-MPDMS:
    - Détection du domicile par analyse des positions nocturnes
    - Migration = changement de résidence > 50km pendant > 30 jours
    - Classification par type de migration
    """

    # Classification UN des types de migration
    MIGRATION_TYPES = {
        "long_distance": "Distance > 200km",
        "regional": "Distance 50-200km",
        "local": "Distance < 50km",
        "return": "Retour au lieu d'origine",
        "circular": "Migration circulaire répétée",
        "seasonal": "Migration saisonnière",
    }

    def __init__(
        self,
        distance_threshold_km: float = 50,
        duration_threshold_days: int = 30,
        confidence_threshold: float = 0.7,
    ):
        """
        Initialise le détecteur

        Args:
            distance_threshold_km: Distance minimale pour considérer une migration
            duration_threshold_days: Durée minimale de présence
            confidence_threshold: Score de confiance minimum
        """
        self.distance_threshold = distance_threshold_km
        self.duration_threshold = duration_threshold_days
        self.confidence_threshold = confidence_threshold

    def detect_home_location(
        self,
        df: pd.DataFrame,
        user_id_col: str = "user_id",
        lat_col: str = "latitude",
        lon_col: str = "longitude",
        timestamp_col: str = "timestamp",
    ) -> pd.DataFrame:
        """
        Détecte le domicile de chaque utilisateur

        Méthode: Mode des positions nocturnes (20h-8h) sur 4 semaines

        Args:
            df: DataFrame avec les positions

        Returns:
            DataFrame avec les domiciles détectés
        """
        logger.info("Détection des domiciles...")

        # Conversion du timestamp si nécessaire
        if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
            df[timestamp_col] = pd.to_datetime(df[timestamp_col])

        # Filtrer les positions nocturnes (20h-8h)
        df["hour"] = df[timestamp_col].dt.hour
        night_positions = df[(df["hour"] >= 20) | (df["hour"] <= 8)].copy()

        if len(night_positions) == 0:
            logger.warning(
                "Pas de positions nocturnes trouvées, utilisation de toutes les positions"
            )
            night_positions = df.copy()

        # Arrondir les coordonnées pour regrouper (précision ~100m)
        night_positions["lat_rounded"] = night_positions[lat_col].round(3)
        night_positions["lon_rounded"] = night_positions[lon_col].round(3)

        # Trouver le mode pour chaque utilisateur
        home_locations = []

        for user_id, user_data in night_positions.groupby(user_id_col):
            # Position la plus fréquente
            location_counts = user_data.groupby(["lat_rounded", "lon_rounded"]).size()

            if len(location_counts) > 0:
                most_common = location_counts.idxmax()
                count = location_counts.max()
                total = len(user_data)

                home_locations.append(
                    {
                        "user_id": user_id,
                        "home_lat": most_common[0],
                        "home_lon": most_common[1],
                        "home_confidence": count / total,
                        "n_observations": total,
                    }
                )

        df_homes = pd.DataFrame(home_locations)
        logger.info(f"✓ {len(df_homes)} domiciles détectés")

        return df_homes

    def detect_migrations(
        self, df: pd.DataFrame, homes_df: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Détecte les événements de migration

        Args:
            df: DataFrame avec les positions ou données de migration
            homes_df: DataFrame avec les domiciles (optionnel)

        Returns:
            DataFrame avec les événements de migration détectés
        """
        logger.info("Détection des migrations...")

        # Si les données contiennent déjà les migrations
        if "origin_district" in df.columns and "current_district" in df.columns:
            migrations = self._process_migration_data(df)
        else:
            # Détection à partir des traces de mobilité
            if homes_df is None:
                homes_df = self.detect_home_location(df)
            migrations = self._detect_from_traces(df, homes_df)

        return migrations

    def _process_migration_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Traite les données de migration existantes

        Args:
            df: DataFrame avec les données de migration

        Returns:
            DataFrame enrichi avec les classifications
        """
        result = df.copy()

        # Classification par distance
        result["migration_class"] = pd.cut(
            result["distance_km"],
            bins=[0, 50, 200, float("inf")],
            labels=["local", "regional", "long_distance"],
        )

        # Score de confiance basé sur la durée
        result["confidence_score"] = np.minimum(
            1.0, result["residence_duration_days"] / 90
        ).round(2)

        # Migration significative
        result["is_significant"] = (
            result["distance_km"] >= self.distance_threshold
        ) & (result["residence_duration_days"] >= self.duration_threshold)

        logger.info(
            f"✓ {result['is_significant'].sum()} migrations significatives détectées"
        )

        return result

    def _detect_from_traces(
        self, traces_df: pd.DataFrame, homes_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Détecte les migrations à partir des traces de mobilité

        Args:
            traces_df: DataFrame avec les traces
            homes_df: DataFrame avec les domiciles

        Returns:
            DataFrame avec les migrations détectées
        """
        # À implémenter: algorithme de fenêtre glissante
        # pour détecter les changements de domicile
        logger.warning(
            "Détection depuis traces non implémentée, utiliser les données de migration"
        )
        return pd.DataFrame()

    def calculate_migration_flows(
        self,
        df: pd.DataFrame,
        origin_col: str = "origin_district",
        dest_col: str = "current_district",
    ) -> pd.DataFrame:
        """
        Calcule les flux migratoires entre zones

        Args:
            df: DataFrame avec les migrations
            origin_col: Colonne d'origine
            dest_col: Colonne de destination

        Returns:
            DataFrame avec les flux O-D
        """
        logger.info("Calcul des flux migratoires...")

        flows = (
            df.groupby([origin_col, dest_col])
            .agg(
                {
                    "user_id": "count",
                    "distance_km": "mean",
                    "residence_duration_days": "mean",
                }
            )
            .reset_index()
        )

        flows.columns = [
            "origin",
            "destination",
            "migration_count",
            "avg_distance_km",
            "avg_duration_days",
        ]

        # Tri par nombre de migrations
        flows = flows.sort_values("migration_count", ascending=False)

        return flows

    def calculate_migration_indicators(
        self, df: pd.DataFrame, population_df: Optional[pd.DataFrame] = None
    ) -> Dict:
        """
        Calcule les indicateurs agrégés de migration

        Args:
            df: DataFrame avec les migrations
            population_df: DataFrame avec la population par zone (optionnel)

        Returns:
            Dictionnaire avec les indicateurs
        """
        logger.info("Calcul des indicateurs de migration...")

        # Filtrer les migrations significatives si la colonne existe
        if "is_significant" in df.columns:
            significant = df[df["is_significant"]]
        else:
            significant = df[
                (df["distance_km"] >= self.distance_threshold)
                & (df["residence_duration_days"] >= self.duration_threshold)
            ]

        indicators = {
            "total_migrations": len(df),
            "significant_migrations": len(significant),
            "mean_distance_km": df["distance_km"].mean(),
            "median_distance_km": df["distance_km"].median(),
            "mean_duration_days": df["residence_duration_days"].mean(),
        }

        # Distribution par type de migration
        if "movement_type" in df.columns:
            indicators["by_type"] = df["movement_type"].value_counts().to_dict()

        # Distribution par classe de distance
        if "migration_class" in df.columns:
            indicators["by_class"] = df["migration_class"].value_counts().to_dict()

        # Taux de migration de retour
        if "is_return_migration" in df.columns:
            indicators["return_migration_rate"] = df["is_return_migration"].mean()

        # Flux nets par zone
        if "origin_district" in df.columns and "current_district" in df.columns:
            in_migration = df.groupby("current_district").size()
            out_migration = df.groupby("origin_district").size()

            all_zones = set(in_migration.index) | set(out_migration.index)
            net_migration = {}

            for zone in all_zones:
                inflow = in_migration.get(zone, 0)
                outflow = out_migration.get(zone, 0)
                net_migration[zone] = {
                    "in_migration": int(inflow),
                    "out_migration": int(outflow),
                    "net_migration": int(inflow - outflow),
                }

            indicators["by_zone"] = net_migration

            # Efficacité migratoire globale
            total_in = in_migration.sum()
            total_out = out_migration.sum()
            gross_migration = total_in + total_out

            if gross_migration > 0:
                indicators["migration_effectiveness"] = (
                    abs(total_in - total_out) / gross_migration
                )

        return indicators

    def generate_od_matrix(
        self, df: pd.DataFrame, zones: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Génère une matrice Origine-Destination

        Args:
            df: DataFrame avec les migrations
            zones: Liste des zones à inclure (optionnel)

        Returns:
            DataFrame avec la matrice O-D
        """
        logger.info("Génération de la matrice O-D...")

        # Création du pivot
        od_matrix = pd.crosstab(
            df["origin_district"],
            df["current_district"],
            margins=True,
            margins_name="Total",
        )

        # Filtrer les zones si spécifié
        if zones:
            zones_with_total = zones + ["Total"]
            od_matrix = od_matrix.loc[
                od_matrix.index.isin(zones_with_total),
                od_matrix.columns.isin(zones_with_total),
            ]

        return od_matrix

    def process(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Process migration data - handles both raw mobility data and pre-computed migration events.
        """
        logger.info("Traitement des données de migration...")

        # Check if this is pre-computed migration data or raw mobility traces
        # Support multiple column naming conventions
        has_origin = any(
            col in df.columns
            for col in [
                "origin_region",
                "origin_district",
                "origin_locality",
                "origin_h3",
            ]
        )
        has_dest = any(
            col in df.columns
            for col in [
                "destination_region",
                "destination_district",
                "current_region",
                "current_district",
                "current_locality",
                "destination_h3",
            ]
        )
        has_type = any(col in df.columns for col in ["migration_type", "movement_type"])
        has_distance = "distance_km" in df.columns

        is_migration_data = has_origin and has_dest and (has_type or has_distance)

        logger.info(f"Colonnes disponibles: {df.columns.tolist()}")
        logger.info(f"Est données de migration pré-calculées: {is_migration_data}")

        if is_migration_data:
            # Data is already migration events - skip detection, just calculate statistics
            logger.info("Données de migration pré-calculées détectées")
            df_migrations = df.copy()

            # Normalize column names for statistics
            if (
                "current_region" in df_migrations.columns
                and "destination_region" not in df_migrations.columns
            ):
                df_migrations["destination_region"] = df_migrations["current_region"]
            if (
                "movement_type" in df_migrations.columns
                and "migration_type" not in df_migrations.columns
            ):
                df_migrations["migration_type"] = df_migrations["movement_type"]

            # Ensure required columns exist
            if "distance_km" not in df_migrations.columns:
                df_migrations["distance_km"] = 0.0
            if "confidence" not in df_migrations.columns:
                df_migrations["confidence"] = 0.8
        else:
            # Raw mobility data - detect migrations
            logger.info("Données de mobilité brutes - détection des migrations...")
            df_migrations = self.detect_migrations(df)

        # Calculate statistics
        stats = self.calculate_migration_statistics(df_migrations)

        logger.info(f"✓ {len(df_migrations)} migrations traitées")
        return df_migrations, stats

    def calculate_migration_statistics(self, df: pd.DataFrame) -> Dict:
        """Calcule les statistiques agrégées de migration."""
        logger.info("Calcul des statistiques de migration...")

        if df.empty:
            return {
                "total_migrations": 0,
                "by_type": {},
                "by_region": {},
                "temporal": {},
            }

        stats = {
            "total_migrations": len(df),
            "by_type": {},
            "by_region": {},
            "temporal": {},
        }

        # Par type de migration (support both column names)
        type_col = (
            "migration_type"
            if "migration_type" in df.columns
            else "movement_type" if "movement_type" in df.columns else None
        )
        if type_col:
            stats["by_type"] = df[type_col].value_counts().to_dict()

        # Par région d'origine (support both column names)
        origin_col = next(
            (c for c in ["origin_region", "origin_district"] if c in df.columns), None
        )
        if origin_col:
            stats["by_region"]["origin"] = df[origin_col].value_counts().to_dict()

        # Par région de destination (support both column names)
        dest_col = next(
            (
                c
                for c in [
                    "destination_region",
                    "destination_district",
                    "current_district",
                ]
                if c in df.columns
            ),
            None,
        )
        if dest_col:
            stats["by_region"]["destination"] = df[dest_col].value_counts().to_dict()

        # Statistiques temporelles
        date_col = next(
            (
                c
                for c in ["detection_date", "timestamp", "migration_date"]
                if c in df.columns
            ),
            None,
        )
        if date_col:
            df_temp = df.copy()
            df_temp[date_col] = pd.to_datetime(df_temp[date_col])
            stats["temporal"]["by_month"] = (
                df_temp.groupby(df_temp[date_col].dt.to_period("M")).size().to_dict()
            )
            stats["temporal"]["by_month"] = {
                str(k): v for k, v in stats["temporal"]["by_month"].items()
            }

        # Distance moyenne si disponible
        if "distance_km" in df.columns:
            stats["avg_distance_km"] = float(df["distance_km"].mean())

        logger.info(f"✓ Statistiques calculées: {stats['total_migrations']} migrations")
        return stats


def main():
    """Test du module"""
    # Données de test
    np.random.seed(42)
    n = 50

    cities = ["Abidjan", "Bouaké", "Korhogo", "San-Pedro", "Yamoussoukro"]

    test_data = pd.DataFrame(
        {
            "user_id": [f"USR_{i:03d}" for i in range(n)],
            "timestamp": pd.date_range("2024-01-01", periods=n, freq="D"),
            "origin_district": np.random.choice(cities, n),
            "current_district": np.random.choice(cities, n),
            "origin_lat": np.random.uniform(5, 10, n),
            "origin_lon": np.random.uniform(-8, -4, n),
            "current_lat": np.random.uniform(5, 10, n),
            "current_lon": np.random.uniform(-8, -4, n),
            "residence_duration_days": np.random.randint(10, 200, n),
            "movement_type": np.random.choice(
                ["permanent_relocation", "work_migration", "seasonal_agriculture"], n
            ),
            "is_return_migration": np.random.choice([True, False], n, p=[0.3, 0.7]),
            "distance_km": np.random.exponential(150, n),
        }
    )

    # Analyse
    detector = MigrationDetector()
    df_result, indicators = detector.process(test_data)

    print("\n=== Résultats ===")
    print(f"Total migrations: {indicators['total_migrations']}")
    print(f"Migrations significatives: {indicators['significant_migrations']}")
    print(f"Distance moyenne: {indicators['mean_distance_km']:.1f} km")

    if "by_type" in indicators:
        print("\nPar type de migration:")
        for mtype, count in indicators["by_type"].items():
            print(f"  {mtype}: {count}")


if __name__ == "__main__":
    main()
