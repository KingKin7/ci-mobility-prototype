"""
Calculateur de métriques de mobilité quotidienne
Conforme aux standards UN-MPDMIS (Mobile Positioning Data for Mobility and Infrastructure Statistics)

Ce module calcule les indicateurs de mobilité urbaine et interurbaine
à partir des données de déplacements.
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from loguru import logger


class MobilityMetrics:
    """
    Calcule les métriques de mobilité selon les standards UN-MPDMIS
    
    Indicateurs:
    - Matrices Origine-Destination
    - Temps de trajet moyens
    - Répartition modale
    - Indice de congestion
    - Accessibilité (SDG 11.2.1)
    """
    
    # Modes de transport et vitesses typiques
    TRANSPORT_MODES = {
        'walking': {'speed_range': (3, 7), 'co2_factor': 0},
        'bicycle': {'speed_range': (8, 20), 'co2_factor': 0},
        'bus': {'speed_range': (10, 30), 'co2_factor': 89},
        'taxi': {'speed_range': (15, 45), 'co2_factor': 171},
        'motorbike': {'speed_range': (15, 40), 'co2_factor': 103},
        'personal_car': {'speed_range': (20, 60), 'co2_factor': 171}
    }
    
    def __init__(self, h3_resolution: int = 7):
        """
        Initialise le calculateur
        
        Args:
            h3_resolution: Résolution H3 pour l'agrégation spatiale
        """
        self.h3_resolution = h3_resolution
    
    def calculate_od_matrix(
        self,
        df: pd.DataFrame,
        origin_col: str = 'origin_antenna',
        dest_col: str = 'dest_antenna',
        time_filter: Optional[Tuple[int, int]] = None
    ) -> pd.DataFrame:
        """
        Calcule la matrice Origine-Destination
        
        Args:
            df: DataFrame avec les trajets
            origin_col: Colonne d'origine
            dest_col: Colonne de destination
            time_filter: Tuple (heure_début, heure_fin) pour filtrer
            
        Returns:
            DataFrame avec la matrice O-D agrégée
        """
        logger.info("Calcul de la matrice Origine-Destination...")
        
        data = df.copy()
        
        # Filtrage temporel
        if time_filter and 'hour_of_day' in data.columns:
            start_hour, end_hour = time_filter
            data = data[
                (data['hour_of_day'] >= start_hour) &
                (data['hour_of_day'] <= end_hour)
            ]
        
        # Agrégation par paire O-D
        od_agg = data.groupby([origin_col, dest_col]).agg({
            'trip_id': 'count',
            'duration_min': ['mean', 'std'],
            'distance_km': ['mean', 'sum'],
            'speed_kmh': 'mean'
        }).reset_index()
        
        # Aplatir les colonnes multi-niveau
        od_agg.columns = [
            'origin', 'destination', 'trips',
            'avg_duration_min', 'std_duration_min',
            'avg_distance_km', 'total_distance_km',
            'avg_speed_kmh'
        ]
        
        # Trier par nombre de trajets
        od_agg = od_agg.sort_values('trips', ascending=False)
        
        logger.info(f"✓ Matrice O-D calculée: {len(od_agg)} paires uniques")
        
        return od_agg
    
    def calculate_modal_split(self, df: pd.DataFrame) -> Dict:
        """
        Calcule la répartition modale des déplacements
        
        Args:
            df: DataFrame avec les trajets
            
        Returns:
            Dictionnaire avec la répartition par mode
        """
        logger.info("Calcul de la répartition modale...")
        
        if 'transport_mode' not in df.columns:
            logger.warning("Colonne transport_mode absente")
            return {}
        
        # Comptage par mode
        mode_counts = df['transport_mode'].value_counts()
        total = len(df)
        
        modal_split = {}
        for mode, count in mode_counts.items():
            modal_split[mode] = {
                'count': int(count),
                'percentage': round(count / total * 100, 1),
                'avg_distance_km': round(
                    df[df['transport_mode'] == mode]['distance_km'].mean(), 2
                ),
                'avg_duration_min': round(
                    df[df['transport_mode'] == mode]['duration_min'].mean(), 1
                )
            }
        
        # Modes actifs vs motorisés
        active_modes = ['walking', 'bicycle']
        public_modes = ['bus']
        private_modes = ['taxi', 'motorbike', 'personal_car']
        
        modal_split['summary'] = {
            'active_transport': round(
                df[df['transport_mode'].isin(active_modes)].shape[0] / total * 100, 1
            ),
            'public_transport': round(
                df[df['transport_mode'].isin(public_modes)].shape[0] / total * 100, 1
            ),
            'private_transport': round(
                df[df['transport_mode'].isin(private_modes)].shape[0] / total * 100, 1
            )
        }
        
        return modal_split
    
    def calculate_commute_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calcule les statistiques de navettage domicile-travail
        
        Args:
            df: DataFrame avec les trajets
            
        Returns:
            Dictionnaire avec les statistiques
        """
        logger.info("Calcul des statistiques de navettage...")
        
        # Filtrer les trajets domicile-travail
        if 'trip_purpose' in df.columns:
            commute_trips = df[
                df['trip_purpose'].isin(['home_to_work', 'work_to_home'])
            ]
        else:
            # Approximation: trajets aux heures de pointe
            if 'hour_of_day' in df.columns:
                commute_trips = df[
                    ((df['hour_of_day'] >= 6) & (df['hour_of_day'] <= 9)) |
                    ((df['hour_of_day'] >= 17) & (df['hour_of_day'] <= 20))
                ]
            else:
                commute_trips = df
        
        if len(commute_trips) == 0:
            return {'error': 'Pas de trajets de navettage trouvés'}
        
        stats = {
            'total_commute_trips': len(commute_trips),
            'avg_commute_time_min': round(commute_trips['duration_min'].mean(), 1),
            'median_commute_time_min': round(commute_trips['duration_min'].median(), 1),
            'avg_commute_distance_km': round(commute_trips['distance_km'].mean(), 2),
            'p90_commute_time_min': round(commute_trips['duration_min'].quantile(0.9), 1),
        }
        
        # Par période
        if 'hour_of_day' in commute_trips.columns:
            morning = commute_trips[
                (commute_trips['hour_of_day'] >= 6) &
                (commute_trips['hour_of_day'] <= 9)
            ]
            evening = commute_trips[
                (commute_trips['hour_of_day'] >= 17) &
                (commute_trips['hour_of_day'] <= 20)
            ]
            
            stats['morning_peak'] = {
                'avg_duration_min': round(morning['duration_min'].mean(), 1) if len(morning) > 0 else None,
                'trips_count': len(morning)
            }
            stats['evening_peak'] = {
                'avg_duration_min': round(evening['duration_min'].mean(), 1) if len(evening) > 0 else None,
                'trips_count': len(evening)
            }
        
        return stats
    
    def calculate_congestion_index(
        self,
        df: pd.DataFrame,
        free_flow_speed: float = 40.0
    ) -> pd.DataFrame:
        """
        Calcule l'indice de congestion par zone et heure
        
        L'indice de congestion = temps réel / temps en flux libre
        
        Args:
            df: DataFrame avec les trajets
            free_flow_speed: Vitesse en flux libre (km/h)
            
        Returns:
            DataFrame avec les indices de congestion
        """
        logger.info("Calcul de l'indice de congestion...")
        
        data = df.copy()
        
        # Temps de trajet en flux libre
        data['free_flow_time_min'] = (data['distance_km'] / free_flow_speed) * 60
        
        # Indice de congestion
        data['congestion_index'] = data['duration_min'] / data['free_flow_time_min'].clip(lower=1)
        
        # Agrégation par heure
        if 'hour_of_day' in data.columns:
            hourly_congestion = data.groupby('hour_of_day').agg({
                'congestion_index': ['mean', 'std'],
                'speed_kmh': 'mean',
                'trip_id': 'count'
            }).reset_index()
            
            hourly_congestion.columns = [
                'hour_of_day', 'avg_congestion', 'std_congestion',
                'avg_speed_kmh', 'trip_count'
            ]
            
            return hourly_congestion
        
        return data[['trip_id', 'congestion_index', 'duration_min', 'free_flow_time_min']]
    
    def calculate_accessibility(
        self,
        df: pd.DataFrame,
        public_transport_threshold_min: float = 30.0
    ) -> Dict:
        """
        Calcule l'accessibilité aux transports publics (SDG 11.2.1)
        
        SDG 11.2.1: Proportion de la population ayant accès aux transports publics
        
        Args:
            df: DataFrame avec les trajets
            public_transport_threshold_min: Seuil de temps d'accès (minutes)
            
        Returns:
            Dictionnaire avec les métriques d'accessibilité
        """
        logger.info("Calcul de l'accessibilité aux transports...")
        
        # Trajets en transport public
        public_modes = ['bus']
        
        if 'transport_mode' not in df.columns:
            return {'error': 'Données de mode de transport manquantes'}
        
        # Utilisateurs ayant utilisé les transports publics
        public_users = df[df['transport_mode'].isin(public_modes)]['user_id'].unique()
        all_users = df['user_id'].unique()
        
        # Approximation du taux d'accès
        access_rate = len(public_users) / len(all_users)
        
        # Classification par niveau d'accessibilité
        user_accessibility = df.groupby('user_id').apply(
            lambda x: 'Good' if x['transport_mode'].isin(public_modes).any()
            and x['duration_min'].min() <= public_transport_threshold_min
            else 'Moderate' if x['duration_min'].min() <= 45
            else 'Poor'
        ).reset_index(name='accessibility_level')
        
        accessibility_dist = user_accessibility['accessibility_level'].value_counts(normalize=True)
        
        result = {
            'sdg_11_2_1': round(access_rate, 3),  # Proportion avec accès
            'public_transport_usage_rate': round(
                df[df['transport_mode'].isin(public_modes)].shape[0] / len(df), 3
            ),
            'accessibility_distribution': accessibility_dist.to_dict(),
            'avg_public_transport_time_min': round(
                df[df['transport_mode'].isin(public_modes)]['duration_min'].mean(), 1
            ) if len(df[df['transport_mode'].isin(public_modes)]) > 0 else None
        }
        
        return result
    
    def calculate_daily_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyse les patterns de mobilité par heure de la journée
        
        Args:
            df: DataFrame avec les trajets
            
        Returns:
            DataFrame avec les patterns horaires
        """
        logger.info("Analyse des patterns horaires...")
        
        if 'hour_of_day' not in df.columns:
            logger.warning("Colonne hour_of_day absente")
            return pd.DataFrame()
        
        hourly_stats = df.groupby('hour_of_day').agg({
            'trip_id': 'count',
            'distance_km': ['mean', 'sum'],
            'duration_min': 'mean',
            'speed_kmh': 'mean'
        }).reset_index()
        
        hourly_stats.columns = [
            'hour', 'trip_count', 'avg_distance_km', 'total_distance_km',
            'avg_duration_min', 'avg_speed_kmh'
        ]
        
        # Identifier les périodes de pointe
        max_trips = hourly_stats['trip_count'].max()
        hourly_stats['is_peak_hour'] = hourly_stats['trip_count'] > (max_trips * 0.7)
        
        return hourly_stats
    
    def calculate_carbon_footprint(self, df: pd.DataFrame) -> Dict:
        """
        Estime l'empreinte carbone des déplacements
        
        Args:
            df: DataFrame avec les trajets
            
        Returns:
            Dictionnaire avec les métriques carbone
        """
        logger.info("Calcul de l'empreinte carbone...")
        
        if 'transport_mode' not in df.columns:
            return {'error': 'Données de mode de transport manquantes'}
        
        data = df.copy()
        
        # Ajout du facteur CO2 par mode
        data['co2_factor'] = data['transport_mode'].map(
            {mode: info['co2_factor'] for mode, info in self.TRANSPORT_MODES.items()}
        ).fillna(100)  # Valeur par défaut
        
        # Calcul des émissions (g CO2)
        data['co2_emissions_g'] = data['distance_km'] * data['co2_factor']
        
        result = {
            'total_co2_kg': round(data['co2_emissions_g'].sum() / 1000, 2),
            'avg_co2_per_trip_g': round(data['co2_emissions_g'].mean(), 1),
            'by_mode': {}
        }
        
        for mode in data['transport_mode'].unique():
            mode_data = data[data['transport_mode'] == mode]
            result['by_mode'][mode] = {
                'total_co2_kg': round(mode_data['co2_emissions_g'].sum() / 1000, 2),
                'avg_co2_per_trip_g': round(mode_data['co2_emissions_g'].mean(), 1),
                'trips_count': len(mode_data)
            }
        
        return result
    
    def process(self, df: pd.DataFrame) -> Tuple[Dict, Dict]:
        """
        Pipeline complet de calcul des métriques de mobilité
        
        Args:
            df: DataFrame avec les trajets
            
        Returns:
            Tuple (métriques détaillées, indicateurs agrégés)
        """
        logger.info("=== Analyse complète de la mobilité ===")
        
        # 1. Matrice O-D
        od_matrix = self.calculate_od_matrix(df)
        
        # 2. Répartition modale
        modal_split = self.calculate_modal_split(df)
        
        # 3. Statistiques de navettage
        commute_stats = self.calculate_commute_statistics(df)
        
        # 4. Congestion
        congestion = self.calculate_congestion_index(df)
        
        # 5. Accessibilité
        accessibility = self.calculate_accessibility(df)
        
        # 6. Patterns journaliers
        daily_patterns = self.calculate_daily_patterns(df)
        
        # 7. Empreinte carbone
        carbon = self.calculate_carbon_footprint(df)
        
        # Résultats détaillés
        detailed = {
            'od_matrix': od_matrix,
            'congestion_data': congestion,
            'daily_patterns': daily_patterns
        }
        
        # Indicateurs agrégés
        indicators = {
            'total_trips': len(df),
            'unique_users': df['user_id'].nunique() if 'user_id' in df.columns else None,
            'total_distance_km': round(df['distance_km'].sum(), 2),
            'avg_trip_distance_km': round(df['distance_km'].mean(), 2),
            'avg_trip_duration_min': round(df['duration_min'].mean(), 1),
            'modal_split': modal_split,
            'commute_statistics': commute_stats,
            'accessibility': accessibility,
            'carbon_footprint': carbon
        }
        
        logger.info("✓ Analyse de mobilité terminée")
        
        return detailed, indicators


def main():
    """Test du module"""
    np.random.seed(42)
    n = 200
    
    modes = ['walking', 'bus', 'taxi', 'motorbike', 'personal_car']
    purposes = ['home_to_work', 'work_to_home', 'shopping', 'leisure']
    
    test_data = pd.DataFrame({
        'user_id': np.random.choice([f'USR_{i:03d}' for i in range(50)], n),
        'trip_id': [f'TRIP_{i:04d}' for i in range(n)],
        'timestamp': pd.date_range('2024-01-15', periods=n, freq='15min'),
        'origin_antenna': np.random.choice([f'ANT_{i:03d}' for i in range(20)], n),
        'dest_antenna': np.random.choice([f'ANT_{i:03d}' for i in range(20)], n),
        'origin_lat': np.random.uniform(5.3, 5.5, n),
        'origin_lon': np.random.uniform(-4.1, -3.9, n),
        'dest_lat': np.random.uniform(5.3, 5.5, n),
        'dest_lon': np.random.uniform(-4.1, -3.9, n),
        'distance_km': np.random.exponential(5, n),
        'duration_min': np.random.exponential(20, n),
        'speed_kmh': np.random.uniform(5, 40, n),
        'transport_mode': np.random.choice(modes, n, p=[0.2, 0.25, 0.2, 0.2, 0.15]),
        'trip_purpose': np.random.choice(purposes, n),
        'hour_of_day': np.random.choice(range(6, 22), n)
    })
    
    # Analyse
    metrics = MobilityMetrics()
    detailed, indicators = metrics.process(test_data)
    
    print("\n=== Résultats ===")
    print(f"Total trajets: {indicators['total_trips']}")
    print(f"Distance totale: {indicators['total_distance_km']:.0f} km")
    print(f"Distance moyenne: {indicators['avg_trip_distance_km']:.1f} km")
    print(f"Durée moyenne: {indicators['avg_trip_duration_min']:.0f} min")
    
    if 'modal_split' in indicators and 'summary' in indicators['modal_split']:
        print("\nRépartition modale:")
        for cat, pct in indicators['modal_split']['summary'].items():
            print(f"  {cat}: {pct}%")


if __name__ == "__main__":
    main()
