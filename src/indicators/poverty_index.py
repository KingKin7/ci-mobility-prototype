"""
Calculateur d'indicateurs de pauvreté
Conforme aux standards UN et méthodologie DHS/LSMS

Ce module calcule un indice de richesse multidimensionnel
à partir des données de téléphonie mobile.
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class PovertyIndexCalculator:
    """
    Calcule les indicateurs de pauvreté à partir des données télécom
    
    Méthodologie basée sur:
    - Blumenstock et al. (2015)
    - UN Guidelines for Mobile Phone Data
    - DHS Wealth Index methodology
    """
    
    def __init__(self):
        """Initialise le calculateur"""
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=1)
        self.is_fitted = False
        
        # Variables utilisées pour le calcul
        self.feature_columns = [
            'recharge_amount_fcfa',
            'recharge_frequency_weekly',
            'call_duration_sec',
            'data_mb',
            'contact_diversity_score',
            'mobility_radius_km'
        ]
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prépare les features pour le calcul de l'indice
        
        Args:
            df: DataFrame avec les données brutes
            
        Returns:
            DataFrame avec les features préparées
        """
        logger.info("Préparation des features pour l'indice de pauvreté...")
        
        # Agrégation par utilisateur si nécessaire
        if 'week_start' in df.columns:
            agg_dict = {
                'recharge_amount_fcfa': 'mean',
                'recharge_frequency_weekly': 'mean',
                'call_duration_sec': 'mean',
                'data_mb': 'mean',
                'contact_diversity_score': 'mean',
                'mobility_radius_km': 'mean'
            }
            
            # Ajouter les colonnes catégorielles si présentes
            if 'phone_type' in df.columns:
                agg_dict['phone_type'] = 'first'
            if 'subscription_type' in df.columns:
                agg_dict['subscription_type'] = 'first'
            if 'district' in df.columns:
                agg_dict['district'] = 'first'
            
            df_agg = df.groupby('user_id').agg(agg_dict).reset_index()
        else:
            df_agg = df.copy()
        
        # Transformation logarithmique pour les variables de montant
        for col in ['recharge_amount_fcfa', 'call_duration_sec', 'data_mb']:
            if col in df_agg.columns:
                df_agg[f'{col}_log'] = np.log1p(df_agg[col])
        
        # Encodage des variables catégorielles
        if 'phone_type' in df_agg.columns:
            phone_map = {'basic': 0, 'feature': 1, 'smartphone': 2}
            df_agg['phone_type_encoded'] = df_agg['phone_type'].map(phone_map).fillna(1)
        
        if 'subscription_type' in df_agg.columns:
            sub_map = {'prepaid': 0, 'postpaid': 1}
            df_agg['subscription_encoded'] = df_agg['subscription_type'].map(sub_map).fillna(0)
        
        return df_agg
    
    def calculate_wealth_index(
        self,
        df: pd.DataFrame,
        method: str = 'pca'
    ) -> pd.DataFrame:
        """
        Calcule l'indice de richesse
        
        Args:
            df: DataFrame préparé
            method: Méthode de calcul ('pca' ou 'simple')
            
        Returns:
            DataFrame avec l'indice de richesse ajouté
        """
        logger.info(f"Calcul de l'indice de richesse (méthode: {method})...")
        
        # Sélection des features numériques
        feature_cols = []
        for col in self.feature_columns:
            if col in df.columns:
                feature_cols.append(col)
            # Aussi les versions log
            log_col = f'{col}_log'
            if log_col in df.columns:
                feature_cols.append(log_col)
        
        # Ajouter les encodages
        for col in ['phone_type_encoded', 'subscription_encoded']:
            if col in df.columns:
                feature_cols.append(col)
        
        # Création de la matrice de features
        X = df[feature_cols].fillna(df[feature_cols].median())
        
        if method == 'pca':
            # Standardisation
            X_scaled = self.scaler.fit_transform(X)
            
            # PCA pour extraire la première composante
            wealth_scores = self.pca.fit_transform(X_scaled)
            
            # Normalisation 0-1
            wealth_scores_norm = (wealth_scores - wealth_scores.min()) / \
                                (wealth_scores.max() - wealth_scores.min())
            
            df['wealth_index'] = wealth_scores_norm.flatten()
            
            # Variance expliquée
            var_explained = self.pca.explained_variance_ratio_[0]
            logger.info(f"Variance expliquée par PC1: {var_explained:.2%}")
            
        else:  # Simple weighted average
            # Poids égaux normalisés
            weights = {col: 1/len(feature_cols) for col in feature_cols}
            
            # Normalisation min-max pour chaque feature
            X_norm = (X - X.min()) / (X.max() - X.min())
            
            # Score moyen pondéré
            df['wealth_index'] = X_norm.mean(axis=1)
        
        self.is_fitted = True
        
        return df
    
    def assign_quintiles(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Assigne les quintiles de richesse
        
        Args:
            df: DataFrame avec wealth_index
            
        Returns:
            DataFrame avec les quintiles ajoutés
        """
        logger.info("Assignation des quintiles de richesse...")
        
        df['wealth_quintile'] = pd.qcut(
            df['wealth_index'],
            q=5,
            labels=['Q1_Poorest', 'Q2', 'Q3', 'Q4', 'Q5_Richest']
        )
        
        # Classification binaire pauvre/non-pauvre (Q1-Q2 = pauvre)
        df['is_poor'] = df['wealth_quintile'].isin(['Q1_Poorest', 'Q2'])
        
        return df
    
    def calculate_poverty_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calcule les statistiques de pauvreté
        
        Args:
            df: DataFrame avec les indicateurs
            
        Returns:
            Dictionnaire avec les statistiques
        """
        logger.info("Calcul des statistiques de pauvreté...")
        
        stats = {
            'total_users': len(df),
            'poverty_rate': df['is_poor'].mean() if 'is_poor' in df.columns else None,
            'mean_wealth_index': df['wealth_index'].mean(),
            'median_wealth_index': df['wealth_index'].median(),
            'std_wealth_index': df['wealth_index'].std(),
        }
        
        # Distribution par quintile
        if 'wealth_quintile' in df.columns:
            stats['quintile_distribution'] = df['wealth_quintile'].value_counts().to_dict()
        
        # Statistiques par district si disponible
        if 'district' in df.columns:
            district_stats = df.groupby('district').agg({
                'wealth_index': ['mean', 'median', 'std'],
                'is_poor': 'mean' if 'is_poor' in df.columns else 'count'
            }).round(3)
            
            stats['by_district'] = district_stats.to_dict()
        
        # Coefficient de Gini simplifié
        wealth_sorted = np.sort(df['wealth_index'].values)
        n = len(wealth_sorted)
        cumulative = np.cumsum(wealth_sorted)
        gini = (n + 1 - 2 * np.sum(cumulative) / cumulative[-1]) / n
        stats['gini_coefficient'] = round(gini, 3)
        
        return stats
    
    def calculate_multidimensional_poverty(
        self,
        df: pd.DataFrame,
        dimensions: Optional[Dict] = None
    ) -> pd.DataFrame:
        """
        Calcule l'indice de pauvreté multidimensionnelle (IPM)
        Méthode Alkire-Foster
        
        Args:
            df: DataFrame avec les indicateurs
            dimensions: Dimensions et seuils personnalisés
            
        Returns:
            DataFrame avec l'IPM
        """
        logger.info("Calcul de l'IPM (méthode Alkire-Foster)...")
        
        if dimensions is None:
            # Dimensions par défaut basées sur les données télécom
            dimensions = {
                'economic': {
                    'indicators': ['recharge_amount_fcfa'],
                    'threshold': 'percentile_20',
                    'weight': 0.4
                },
                'connectivity': {
                    'indicators': ['contact_diversity_score'],
                    'threshold': 0.3,
                    'weight': 0.3
                },
                'mobility': {
                    'indicators': ['mobility_radius_km'],
                    'threshold': 2.0,
                    'weight': 0.3
                }
            }
        
        # Calcul des privations par dimension
        deprivations = []
        
        for dim_name, dim_config in dimensions.items():
            for indicator in dim_config['indicators']:
                if indicator in df.columns:
                    threshold = dim_config['threshold']
                    
                    if isinstance(threshold, str) and 'percentile' in threshold:
                        pct = int(threshold.split('_')[1])
                        threshold_value = df[indicator].quantile(pct / 100)
                    else:
                        threshold_value = threshold
                    
                    # Privation si en dessous du seuil
                    deprived = (df[indicator] < threshold_value).astype(int)
                    deprivations.append(deprived * dim_config['weight'])
        
        if deprivations:
            # Score de privation total
            df['deprivation_score'] = sum(deprivations)
            
            # Pauvre multidimensionnel si score >= 0.33 (1/3 des dimensions)
            df['is_mpi_poor'] = df['deprivation_score'] >= 0.33
            
            # Intensité de la pauvreté
            df['poverty_intensity'] = df.loc[df['is_mpi_poor'], 'deprivation_score'].mean()
        
        return df
    
    def process(
        self,
        df: pd.DataFrame,
        calculate_mpi: bool = True
    ) -> Tuple[pd.DataFrame, Dict]:
        """
        Pipeline complet de calcul des indicateurs de pauvreté
        
        Args:
            df: DataFrame avec les données brutes
            calculate_mpi: Calculer l'IPM en plus
            
        Returns:
            Tuple (DataFrame enrichi, statistiques)
        """
        # 1. Préparation des features
        df_prepared = self.prepare_features(df)
        
        # 2. Calcul de l'indice de richesse
        df_wealth = self.calculate_wealth_index(df_prepared)
        
        # 3. Assignation des quintiles
        df_quintiles = self.assign_quintiles(df_wealth)
        
        # 4. IPM optionnel
        if calculate_mpi:
            df_final = self.calculate_multidimensional_poverty(df_quintiles)
        else:
            df_final = df_quintiles
        
        # 5. Statistiques
        stats = self.calculate_poverty_statistics(df_final)
        
        logger.info("✓ Calcul des indicateurs de pauvreté terminé")
        
        return df_final, stats


def main():
    """Test du module avec des données exemple"""
    # Création de données de test
    np.random.seed(42)
    n = 100
    
    test_data = pd.DataFrame({
        'user_id': [f'USR_{i:03d}' for i in range(n)],
        'recharge_amount_fcfa': np.random.exponential(1000, n),
        'recharge_frequency_weekly': np.random.poisson(3, n),
        'call_duration_sec': np.random.exponential(300, n),
        'data_mb': np.random.exponential(50, n),
        'contact_diversity_score': np.random.beta(2, 5, n),
        'mobility_radius_km': np.random.exponential(5, n),
        'phone_type': np.random.choice(['basic', 'feature', 'smartphone'], n),
        'subscription_type': np.random.choice(['prepaid', 'postpaid'], n, p=[0.85, 0.15]),
        'district': np.random.choice(['Abidjan', 'Bouaké', 'Korhogo'], n)
    })
    
    # Calcul
    calculator = PovertyIndexCalculator()
    df_result, stats = calculator.process(test_data)
    
    print("\n=== Résultats ===")
    print(f"Taux de pauvreté: {stats['poverty_rate']:.1%}")
    print(f"Coefficient de Gini: {stats['gini_coefficient']:.3f}")
    print("\nDistribution par quintile:")
    for q, count in stats['quintile_distribution'].items():
        print(f"  {q}: {count}")


if __name__ == "__main__":
    main()
