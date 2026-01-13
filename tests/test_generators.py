"""
Tests unitaires pour le générateur de données synthétiques
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Ajouter le chemin src
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestSyntheticGenerator:
    """Tests pour le SyntheticDataGenerator"""
    
    @pytest.fixture
    def sample_config(self, tmp_path):
        """Crée un fichier de configuration de test"""
        import yaml
        
        config = {
            'project': {'name': 'Test', 'version': '1.0.0', 'standard': 'TEST'},
            'generation': {
                'n_users': 100,
                'start_date': '2024-01-01',
                'end_date': '2024-01-07',
                'days_to_generate': 7,
                'random_seed': 42
            },
            'spatial_bounds': {
                'min_lat': 4.0, 'max_lat': 11.0,
                'min_lon': -9.0, 'max_lon': -2.0
            },
            'urban_centers': {
                'Abidjan': {'lat': 5.36, 'lon': -4.0, 'weight': 0.5},
                'Bouake': {'lat': 7.68, 'lon': -5.03, 'weight': 0.3},
                'Others': {'lat': 6.5, 'lon': -5.5, 'weight': 0.2}
            },
            'demographics': {
                'age_groups': {'values': ['18-24', '25-34', '35+'], 'probabilities': [0.3, 0.4, 0.3]},
                'gender': {'values': ['M', 'F'], 'probabilities': [0.5, 0.5]},
                'occupation': {'values': ['employee', 'other'], 'probabilities': [0.6, 0.4]},
                'phone_type': {'values': ['basic', 'smartphone'], 'probabilities': [0.5, 0.5]},
                'subscription': {'values': ['prepaid', 'postpaid'], 'probabilities': [0.8, 0.2]}
            },
            'mobility': {'h3_resolution': 7, 'daily_trips_lambda': 3, 'mobility_radius_mean': 5.0, 'mobility_radius_std': 3.0},
            'economic': {
                'recharge_amounts': [100, 500, 1000],
                'recharge_probs_poor': [0.5, 0.3, 0.2],
                'recharge_probs_rich': [0.2, 0.3, 0.5]
            },
            'migration': {'distance_threshold_km': 50, 'duration_threshold_days': 7, 'migration_probability': 0.1},
            'privacy': {'k_anonymity': 10, 'epsilon': 1.0, 'salt_rotation_days': 15},
            'paths': {'output_dir': str(tmp_path / 'output'), 'metadata_dir': str(tmp_path / 'metadata'), 'raw_dir': str(tmp_path / 'raw'), 'processed_dir': str(tmp_path / 'processed')}
        }
        
        config_path = tmp_path / "test_config.yml"
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        
        return str(config_path)
    
    def test_generator_initialization(self, sample_config):
        """Test l'initialisation du générateur"""
        from data_generation.synthetic_generator import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator(sample_config)
        
        assert generator.n_users == 100
        assert generator.days == 7
    
    def test_generate_user_profiles(self, sample_config):
        """Test la génération des profils utilisateurs"""
        from data_generation.synthetic_generator import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator(sample_config)
        users_df = generator.generate_user_profiles()
        
        assert len(users_df) == 100
        assert 'user_id' in users_df.columns
        assert 'age_group' in users_df.columns
        assert 'home_lat' in users_df.columns
        assert 'home_lon' in users_df.columns
        
        # Vérifier que les coordonnées sont dans les limites
        assert users_df['home_lat'].between(4.0, 11.0).all()
        assert users_df['home_lon'].between(-9.0, -2.0).all()
    
    def test_generate_poverty_data(self, sample_config):
        """Test la génération des données de pauvreté"""
        from data_generation.synthetic_generator import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator(sample_config)
        users_df = generator.generate_user_profiles()
        poverty_df = generator.generate_poverty_data(users_df)
        
        assert len(poverty_df) > 0
        assert 'recharge_amount_fcfa' in poverty_df.columns
        assert 'contact_diversity_score' in poverty_df.columns
        
        # Les scores de diversité doivent être entre 0 et 1
        assert poverty_df['contact_diversity_score'].between(0, 1).all()
    
    def test_generate_migration_data(self, sample_config):
        """Test la génération des données de migration"""
        from data_generation.synthetic_generator import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator(sample_config)
        users_df = generator.generate_user_profiles()
        migration_df = generator.generate_migration_data(users_df)
        
        # Environ 10% des utilisateurs migrent
        assert len(migration_df) <= len(users_df) * 0.2
        
        if len(migration_df) > 0:
            assert 'origin_district' in migration_df.columns
            assert 'current_district' in migration_df.columns
            assert 'distance_km' in migration_df.columns


class TestPovertyIndex:
    """Tests pour le calculateur d'indice de pauvreté"""
    
    @pytest.fixture
    def sample_data(self):
        """Crée des données de test"""
        np.random.seed(42)
        n = 50
        
        return pd.DataFrame({
            'user_id': [f'USR_{i:03d}' for i in range(n)],
            'recharge_amount_fcfa': np.random.exponential(1000, n),
            'recharge_frequency_weekly': np.random.poisson(3, n),
            'call_duration_sec': np.random.exponential(300, n),
            'data_mb': np.random.exponential(50, n),
            'contact_diversity_score': np.random.beta(2, 5, n),
            'mobility_radius_km': np.random.exponential(5, n),
            'phone_type': np.random.choice(['basic', 'feature', 'smartphone'], n),
            'subscription_type': np.random.choice(['prepaid', 'postpaid'], n),
            'district': np.random.choice(['Abidjan', 'Bouake'], n)
        })
    
    def test_wealth_index_calculation(self, sample_data):
        """Test le calcul de l'indice de richesse"""
        from indicators.poverty_index import PovertyIndexCalculator
        
        calculator = PovertyIndexCalculator()
        df_result, stats = calculator.process(sample_data)
        
        assert 'wealth_index' in df_result.columns
        assert df_result['wealth_index'].between(0, 1).all()
        assert 'wealth_quintile' in df_result.columns
    
    def test_poverty_statistics(self, sample_data):
        """Test le calcul des statistiques de pauvreté"""
        from indicators.poverty_index import PovertyIndexCalculator
        
        calculator = PovertyIndexCalculator()
        _, stats = calculator.process(sample_data)
        
        assert 'poverty_rate' in stats
        assert 'gini_coefficient' in stats
        assert 0 <= stats['poverty_rate'] <= 1
        assert 0 <= stats['gini_coefficient'] <= 1


class TestMobilityMetrics:
    """Tests pour les métriques de mobilité"""
    
    @pytest.fixture
    def sample_trips(self):
        """Crée des données de trajets de test"""
        np.random.seed(42)
        n = 100
        
        return pd.DataFrame({
            'user_id': np.random.choice([f'USR_{i:03d}' for i in range(20)], n),
            'trip_id': [f'TRIP_{i:04d}' for i in range(n)],
            'origin_antenna': np.random.choice([f'ANT_{i:03d}' for i in range(10)], n),
            'dest_antenna': np.random.choice([f'ANT_{i:03d}' for i in range(10)], n),
            'distance_km': np.random.exponential(5, n),
            'duration_min': np.random.exponential(20, n),
            'speed_kmh': np.random.uniform(5, 40, n),
            'transport_mode': np.random.choice(['walking', 'bus', 'taxi'], n),
            'trip_purpose': np.random.choice(['home_to_work', 'shopping'], n),
            'hour_of_day': np.random.choice(range(6, 22), n)
        })
    
    def test_od_matrix(self, sample_trips):
        """Test le calcul de la matrice O-D"""
        from indicators.mobility_metrics import MobilityMetrics
        
        metrics = MobilityMetrics()
        od_matrix = metrics.calculate_od_matrix(sample_trips)
        
        assert len(od_matrix) > 0
        assert 'origin' in od_matrix.columns
        assert 'destination' in od_matrix.columns
        assert 'trips' in od_matrix.columns
    
    def test_modal_split(self, sample_trips):
        """Test le calcul de la répartition modale"""
        from indicators.mobility_metrics import MobilityMetrics
        
        metrics = MobilityMetrics()
        modal_split = metrics.calculate_modal_split(sample_trips)
        
        assert 'walking' in modal_split or 'bus' in modal_split
        
        # Vérifier que les pourcentages totalisent ~100%
        if 'summary' in modal_split:
            total = sum(modal_split['summary'].values())
            assert 99 <= total <= 101


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
