"""
Data Service - Chargement et traitement des données
Couche métier pour le dashboard Django
"""
import os
from pathlib import Path
from typing import Dict, Optional, Any
from functools import lru_cache
import pandas as pd
import numpy as np
from django.conf import settings


class DataService:
    """Service de gestion des données du dashboard"""
    
    # Dictionnaires de traduction
    MIGRATION_TYPE_FR = {
        "work_migration": "Migration travail",
        "seasonal_agriculture": "Agriculture saisonnière",
        "permanent_relocation": "Relocalisation permanente",
        "permanent_relacoation": "Relocalisation permanente",
        "education_migration": "Migration études",
        "circular_migration": "Migration circulaire",
        "return_migration": "Migration retour",
        "family_migration": "Migration familiale",
    }
    
    TRANSPORT_MODE_FR = {
        "walking": "Marche à pied",
        "motorbike": "Moto",
        "taxi": "Taxi",
        "bus": "Bus",
        "personal_car": "Voiture personnelle",
        "bicycle": "Vélo",
        "truck": "Camion",
        "other": "Autre",
    }
    
    TRIP_PURPOSE_FR = {
        "work": "Travail",
        "home": "Domicile",
        "shopping": "Courses",
        "leisure": "Loisirs",
        "education": "Éducation",
        "health": "Santé",
        "family": "Famille",
        "other": "Autre",
    }
    
    FREE_FLOW_SPEEDS = {
        'walking': 5,
        'bicycle': 15,
        'bus': 35,
        'taxi': 45,
        'motorbike': 40,
        'personal_car': 50
    }
    
    def __init__(self):
        self.data_dir = getattr(settings, 'DATA_DIR', Path('data/synthetic'))
        self._cache = {}
    
    def get_data_dir(self) -> Path:
        """Retourne le chemin du dossier de données"""
        return Path(self.data_dir)
    
    def load_all_datasets(self, force_reload: bool = False) -> Dict[str, pd.DataFrame]:
        """Charge tous les datasets disponibles"""
        if not force_reload and self._cache:
            return self._cache
        
        datasets = {}
        data_path = self.get_data_dir()
        
        if not data_path.exists():
            return datasets
        
        for dataset_name in ['users', 'poverty', 'migration', 'mobility']:
            files = list(data_path.glob(f"{dataset_name}_*.csv"))
            if files:
                latest_file = max(files, key=lambda x: x.stat().st_mtime)
                datasets[dataset_name] = pd.read_csv(latest_file)
        
        self._cache = datasets
        return datasets
    
    def get_dataset(self, name: str) -> Optional[pd.DataFrame]:
        """Retourne un dataset spécifique"""
        datasets = self.load_all_datasets()
        return datasets.get(name)
    
    def get_overview_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de la vue d'ensemble"""
        datasets = self.load_all_datasets()
        
        users_df = datasets.get('users', pd.DataFrame())
        poverty_df = datasets.get('poverty', pd.DataFrame())
        migration_df = datasets.get('migration', pd.DataFrame())
        mobility_df = datasets.get('mobility', pd.DataFrame())
        
        # Calcul du taux de pauvreté
        poverty_rate = 0
        if not poverty_df.empty:
            poverty_stats = self.calculate_wealth_index(poverty_df)
            if not poverty_stats.empty and 'is_poor' in poverty_stats.columns:
                poverty_rate = poverty_stats['is_poor'].mean()
        
        # Distribution par région
        region_distribution = []
        if not users_df.empty and 'region' in users_df.columns:
            region_counts = users_df['region'].value_counts().head(15)
            region_distribution = [
                {'region': k, 'count': int(v)} 
                for k, v in region_counts.items()
            ]
        
        # Distribution urbain/rural
        urban_rural = {'urban': 0, 'rural': 0}
        if not users_df.empty and 'urban_rural' in users_df.columns:
            counts = users_df['urban_rural'].value_counts()
            urban_rural = {
                'urban': int(counts.get('urban', 0)),
                'rural': int(counts.get('rural', 0))
            }
        
        # Distribution des types de téléphone
        phone_distribution = []
        if not users_df.empty and 'phone_type' in users_df.columns:
            phone_counts = users_df['phone_type'].value_counts()
            phone_distribution = [
                {'type': k, 'count': int(v), 'percentage': round(v/len(users_df)*100, 1)}
                for k, v in phone_counts.items()
            ]
        
        return {
            'users_count': len(users_df),
            'poverty_rate': round(poverty_rate * 100, 1),
            'migration_count': len(migration_df),
            'mobility_count': len(mobility_df),
            'region_distribution': region_distribution,
            'urban_rural': urban_rural,
            'phone_distribution': phone_distribution,
            'localities_count': users_df['locality'].nunique() if 'locality' in users_df.columns else 0,
            'regions_count': users_df['region'].nunique() if 'region' in users_df.columns else 0,
        }
    
    def calculate_wealth_index(self, poverty_df: pd.DataFrame) -> pd.DataFrame:
        """Calcule l'indice de richesse"""
        if poverty_df.empty:
            return pd.DataFrame()
        
        feature_cols = []
        potential_features = [
            'recharge_amount_fcfa', 'recharge_frequency_weekly',
            'call_duration_sec', 'data_mb',
            'contact_diversity_score', 'mobility_radius_km'
        ]
        
        for col in potential_features:
            if col in poverty_df.columns:
                feature_cols.append(col)
        
        if not feature_cols:
            return pd.DataFrame()
        
        # Agrégation par utilisateur
        agg_dict = {col: 'mean' for col in feature_cols}
        location_cols = ['locality', 'department', 'region', 'latitude', 'longitude']
        for loc_col in location_cols:
            if loc_col in poverty_df.columns:
                agg_dict[loc_col] = 'first'
        
        user_stats = poverty_df.groupby('user_id').agg(agg_dict).reset_index()
        
        # Normalisation min-max
        for col in feature_cols:
            col_min = user_stats[col].min()
            col_max = user_stats[col].max()
            if col_max > col_min:
                user_stats[f'{col}_norm'] = (user_stats[col] - col_min) / (col_max - col_min)
            else:
                user_stats[f'{col}_norm'] = 0.5
        
        # Score de richesse
        norm_cols = [f'{col}_norm' for col in feature_cols]
        user_stats['wealth_index'] = user_stats[norm_cols].mean(axis=1)
        
        # Quintiles
        user_stats['wealth_quintile'] = pd.qcut(
            user_stats['wealth_index'], q=5,
            labels=['Q1_Très pauvre', 'Q2_Pauvre', 'Q3_Moyen', 'Q4_Aisé', 'Q5_Riche']
        )
        
        user_stats['is_poor'] = user_stats['wealth_quintile'].isin(['Q1_Très pauvre', 'Q2_Pauvre'])
        user_stats = user_stats.drop(columns=norm_cols)
        
        return user_stats
    
    def get_poverty_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de pauvreté"""
        poverty_df = self.get_dataset('poverty')
        if poverty_df is None or poverty_df.empty:
            return {}
        
        poverty_stats = self.calculate_wealth_index(poverty_df)
        if poverty_stats.empty:
            return {}
        
        # Statistiques générales
        poverty_rate = poverty_stats['is_poor'].mean() * 100
        avg_recharge = poverty_stats['recharge_amount_fcfa'].mean() if 'recharge_amount_fcfa' in poverty_stats.columns else 0
        avg_mobility = poverty_stats['mobility_radius_km'].mean() if 'mobility_radius_km' in poverty_stats.columns else 0
        avg_diversity = poverty_stats['contact_diversity_score'].mean() if 'contact_diversity_score' in poverty_stats.columns else 0
        
        # Distribution des quintiles
        quintile_distribution = []
        if 'wealth_quintile' in poverty_stats.columns:
            quintile_counts = poverty_stats['wealth_quintile'].value_counts().sort_index()
            quintile_distribution = [
                {'quintile': str(k), 'count': int(v)}
                for k, v in quintile_counts.items()
            ]
        
        # Statistiques par région
        regional_stats = []
        if 'region' in poverty_stats.columns:
            regional = poverty_stats.groupby('region').agg({
                'wealth_index': ['mean', 'std'],
                'user_id': 'count',
                'is_poor': 'mean'
            }).reset_index()
            regional.columns = ['region', 'wealth_mean', 'wealth_std', 'population', 'poverty_rate']
            regional = regional.sort_values('wealth_mean')
            
            regional_stats = regional.to_dict('records')
            for r in regional_stats:
                r['poverty_rate'] = round(r['poverty_rate'] * 100, 1)
                r['wealth_mean'] = round(r['wealth_mean'], 3)
        
        # Données pour scatter plot
        scatter_data = []
        if 'mobility_radius_km' in poverty_stats.columns and 'recharge_amount_fcfa' in poverty_stats.columns:
            sample = poverty_stats.sample(min(500, len(poverty_stats)))
            scatter_data = sample[['mobility_radius_km', 'recharge_amount_fcfa', 'wealth_index']].to_dict('records')
        
        return {
            'poverty_rate': round(poverty_rate, 1),
            'avg_recharge': round(avg_recharge, 0),
            'avg_mobility': round(avg_mobility, 1),
            'avg_diversity': round(avg_diversity, 2),
            'quintile_distribution': quintile_distribution,
            'regional_stats': regional_stats,
            'scatter_data': scatter_data,
            'wealth_distribution': poverty_stats['wealth_index'].describe().to_dict()
        }
    
    def get_migration_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de migration"""
        migration_df = self.get_dataset('migration')
        if migration_df is None or migration_df.empty:
            return {}
        
        # Statistiques générales
        stats = {
            'total_migrations': len(migration_df),
            'avg_distance': round(migration_df['distance_km'].mean(), 1),
            'median_distance': round(migration_df['distance_km'].median(), 1),
            'avg_duration': round(migration_df['residence_duration_days'].mean(), 0),
            'return_rate': round(migration_df['is_return_migration'].mean() * 100, 1),
        }
        
        # Types de migration
        type_distribution = []
        if 'movement_type' in migration_df.columns:
            type_counts = migration_df['movement_type'].value_counts()
            type_distribution = [
                {
                    'type': self.MIGRATION_TYPE_FR.get(k, k),
                    'type_en': k,
                    'count': int(v),
                    'percentage': round(v / len(migration_df) * 100, 1)
                }
                for k, v in type_counts.items()
            ]
        
        # Corridors migratoires
        corridors = []
        if 'origin_locality' in migration_df.columns and 'current_locality' in migration_df.columns:
            flows = migration_df.groupby(['origin_locality', 'current_locality']).size().reset_index(name='count')
            flows = flows.sort_values('count', ascending=False).head(15)
            corridors = [
                {
                    'origin': row['origin_locality'],
                    'destination': row['current_locality'],
                    'corridor': f"{row['origin_locality']} → {row['current_locality']}",
                    'count': int(row['count'])
                }
                for _, row in flows.iterrows()
            ]
        
        # Matrice O-D par région
        od_matrix = []
        if 'origin_region' in migration_df.columns and 'current_region' in migration_df.columns:
            matrix = pd.crosstab(migration_df['origin_region'], migration_df['current_region'])
            od_matrix = {
                'regions': matrix.columns.tolist(),
                'data': matrix.values.tolist(),
                'index': matrix.index.tolist()
            }
        
        # Distribution des distances
        distance_histogram = migration_df['distance_km'].value_counts(bins=20).sort_index()
        distance_distribution = [
            {'bin': f"{int(interval.left)}-{int(interval.right)}", 'count': int(count)}
            for interval, count in distance_histogram.items()
        ]
        
        return {
            **stats,
            'type_distribution': type_distribution,
            'corridors': corridors,
            'od_matrix': od_matrix,
            'distance_distribution': distance_distribution
        }
    
    def get_mobility_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de mobilité"""
        mobility_df = self.get_dataset('mobility')
        if mobility_df is None or mobility_df.empty:
            return {}
        
        # Calculer l'indice de congestion
        mobility_df = mobility_df.copy()
        mobility_df['free_flow_speed'] = mobility_df['transport_mode'].map(self.FREE_FLOW_SPEEDS).fillna(30)
        mobility_df['congestion_index'] = mobility_df['free_flow_speed'] / mobility_df['speed_kmh'].clip(lower=1)
        mobility_df['congestion_index'] = mobility_df['congestion_index'].clip(upper=5)
        
        # Statistiques générales
        stats = {
            'total_trips': len(mobility_df),
            'avg_distance': round(mobility_df['distance_km'].mean(), 2),
            'avg_duration': round(mobility_df['duration_min'].mean(), 1),
            'avg_speed': round(mobility_df['speed_kmh'].mean(), 1),
        }
        
        # Distribution modale
        mode_distribution = []
        if 'transport_mode' in mobility_df.columns:
            mode_counts = mobility_df['transport_mode'].value_counts()
            mode_distribution = [
                {
                    'mode': self.TRANSPORT_MODE_FR.get(k, k),
                    'mode_en': k,
                    'count': int(v),
                    'percentage': round(v / len(mobility_df) * 100, 1)
                }
                for k, v in mode_counts.items()
            ]
        
        # Motifs de déplacement
        purpose_distribution = []
        if 'trip_purpose' in mobility_df.columns:
            purpose_counts = mobility_df['trip_purpose'].value_counts()
            purpose_distribution = [
                {
                    'purpose': self.TRIP_PURPOSE_FR.get(k, k),
                    'purpose_en': k,
                    'count': int(v),
                    'percentage': round(v / len(mobility_df) * 100, 1)
                }
                for k, v in purpose_counts.items()
            ]
        
        # Distribution horaire
        hourly_stats = []
        if 'hour_of_day' in mobility_df.columns:
            hourly = mobility_df.groupby('hour_of_day').agg({
                'trip_id': 'count',
                'congestion_index': 'mean',
                'speed_kmh': 'mean',
                'duration_min': 'mean'
            }).reset_index()
            hourly.columns = ['hour', 'trips', 'congestion', 'speed', 'duration']
            hourly_stats = hourly.to_dict('records')
            
            # Identifier les heures de pointe
            morning_peak = hourly[(hourly['hour'] >= 6) & (hourly['hour'] <= 10)]
            evening_peak = hourly[(hourly['hour'] >= 16) & (hourly['hour'] <= 20)]
            
            stats['morning_peak_hour'] = int(morning_peak.loc[morning_peak['trips'].idxmax(), 'hour']) if not morning_peak.empty else 8
            stats['evening_peak_hour'] = int(evening_peak.loc[evening_peak['trips'].idxmax(), 'hour']) if not evening_peak.empty else 18
            stats['most_congested_hour'] = int(hourly.loc[hourly['congestion'].idxmax(), 'hour'])
            stats['least_congested_hour'] = int(hourly.loc[hourly['congestion'].idxmin(), 'hour'])
        
        # Congestion par zone
        zone_congestion = []
        if 'locality' in mobility_df.columns:
            zone_stats = mobility_df.groupby('locality').agg({
                'trip_id': 'count',
                'speed_kmh': 'mean',
                'congestion_index': 'mean'
            }).reset_index()
            zone_stats.columns = ['locality', 'trips', 'avg_speed', 'congestion']
            zone_stats = zone_stats.sort_values('congestion', ascending=False)
            
            zone_congestion = {
                'most_congested': zone_stats.head(10).to_dict('records'),
                'least_congested': zone_stats.tail(10).sort_values('congestion').to_dict('records')
            }
        
        # Heatmap heure x zone
        heatmap_data = None
        if 'locality' in mobility_df.columns and 'hour_of_day' in mobility_df.columns:
            top_zones = mobility_df['locality'].value_counts().head(15).index.tolist()
            filtered = mobility_df[mobility_df['locality'].isin(top_zones)]
            pivot = filtered.pivot_table(
                values='congestion_index',
                index='locality',
                columns='hour_of_day',
                aggfunc='mean'
            ).fillna(1)
            
            heatmap_data = {
                'hours': pivot.columns.tolist(),
                'localities': pivot.index.tolist(),
                'values': pivot.values.tolist()
            }
        
        # Statistiques par mode
        mode_stats = []
        if 'transport_mode' in mobility_df.columns:
            ms = mobility_df.groupby('transport_mode').agg({
                'distance_km': ['mean', 'sum'],
                'duration_min': 'mean',
                'speed_kmh': 'mean',
                'trip_id': 'count'
            }).round(2)
            ms.columns = ['avg_distance', 'total_distance', 'avg_duration', 'avg_speed', 'trips']
            ms = ms.reset_index()
            ms['transport_mode_fr'] = ms['transport_mode'].map(self.TRANSPORT_MODE_FR)
            mode_stats = ms.to_dict('records')
        
        return {
            **stats,
            'mode_distribution': mode_distribution,
            'purpose_distribution': purpose_distribution,
            'hourly_stats': hourly_stats,
            'zone_congestion': zone_congestion,
            'heatmap_data': heatmap_data,
            'mode_stats': mode_stats
        }
    
    def get_map_data(self) -> Dict[str, Any]:
        """Retourne les données pour la carte interactive"""
        users_df = self.get_dataset('users')
        if users_df is None or users_df.empty:
            return {}
        
        # Points par localité
        locality_points = []
        if 'locality' in users_df.columns and 'home_lat' in users_df.columns:
            locality_agg = users_df.groupby('locality').agg({
                'home_lat': 'mean',
                'home_lon': 'mean',
                'user_id': 'count'
            }).reset_index()
            locality_points = locality_agg.to_dict('records')
        
        # Échantillon de points individuels
        sample_points = []
        if 'home_lat' in users_df.columns:
            sample = users_df.sample(min(500, len(users_df)))
            cols = ['home_lat', 'home_lon']
            if 'locality' in sample.columns:
                cols.append('locality')
            sample_points = sample[cols].to_dict('records')
        
        return {
            'locality_points': locality_points,
            'sample_points': sample_points,
            'center': {'lat': 7.54, 'lon': -5.55},
            'stats': {
                'localities': users_df['locality'].nunique() if 'locality' in users_df.columns else 0,
                'regions': users_df['region'].nunique() if 'region' in users_df.columns else 0,
                'departments': users_df['department'].nunique() if 'department' in users_df.columns else 0,
            }
        }


# Instance singleton du service
data_service = DataService()
