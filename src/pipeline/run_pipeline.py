"""
Pipeline principal d'orchestration
Projet: Mobilité Côte d'Ivoire - ANStat

Ce module orchestre l'ensemble du workflow:
1. Génération des données synthétiques
2. Calcul des indicateurs (pauvreté, migration, mobilité)
3. Export des résultats
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import yaml
from loguru import logger

# Ajout du chemin src pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_generation.synthetic_generator import SyntheticDataGenerator
from indicators.poverty_index import PovertyIndexCalculator
from indicators.migration_flows import MigrationDetector
from indicators.mobility_metrics import MobilityMetrics


class MobilityPipeline:
    """
    Pipeline complet pour l'analyse des données de téléphonie mobile
    """
    
    def __init__(self, config_path: str = "config/data_params.yml"):
        """
        Initialise le pipeline
        
        Args:
            config_path: Chemin vers la configuration
        """
        self.config_path = Path(config_path)
        self._load_config()
        self._setup_logging()
        
        # Initialisation des composants
        self.generator = SyntheticDataGenerator(str(config_path))
        self.poverty_calc = PovertyIndexCalculator()
        self.migration_detector = MigrationDetector()
        self.mobility_metrics = MobilityMetrics()
        
        # Stockage des résultats
        self.datasets = {}
        self.indicators = {}
        self.detailed_results = {}
        
        logger.info("Pipeline initialisé")
    
    def _load_config(self) -> None:
        """Charge la configuration"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
    
    def _setup_logging(self) -> None:
        """Configure le logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logger.add(
            log_dir / "pipeline_{time}.log",
            rotation="1 day",
            retention="7 days",
            level="INFO",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
        )
    
    def step_1_generate_data(self, save: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Étape 1: Génération des données synthétiques
        
        Args:
            save: Sauvegarder les fichiers
            
        Returns:
            Dictionnaire avec les datasets
        """
        logger.info("=" * 50)
        logger.info("ÉTAPE 1: Génération des données synthétiques")
        logger.info("=" * 50)
        
        self.datasets = self.generator.generate_all(save=save)
        
        # Résumé
        for name, df in self.datasets.items():
            logger.info(f"  {name}: {len(df)} enregistrements")
        
        return self.datasets
    
    def step_2_calculate_indicators(self) -> Dict:
        """
        Étape 2: Calcul des indicateurs
        
        Returns:
            Dictionnaire avec tous les indicateurs
        """
        logger.info("=" * 50)
        logger.info("ÉTAPE 2: Calcul des indicateurs")
        logger.info("=" * 50)
        
        # 2.1 Indicateurs de pauvreté
        logger.info("-" * 30)
        logger.info("2.1 Indicateurs de pauvreté")
        
        if 'poverty' in self.datasets:
            poverty_df, poverty_stats = self.poverty_calc.process(
                self.datasets['poverty']
            )
            self.datasets['poverty_enriched'] = poverty_df
            self.indicators['poverty'] = poverty_stats
        
        # 2.2 Indicateurs de migration
        logger.info("-" * 30)
        logger.info("2.2 Indicateurs de migration")
        
        if 'migration' in self.datasets:
            migration_df, migration_stats = self.migration_detector.process(
                self.datasets['migration']
            )
            self.datasets['migration_enriched'] = migration_df
            self.indicators['migration'] = migration_stats
        
        # 2.3 Indicateurs de mobilité
        logger.info("-" * 30)
        logger.info("2.3 Indicateurs de mobilité")
        
        if 'mobility' in self.datasets:
            detailed, mobility_stats = self.mobility_metrics.process(
                self.datasets['mobility']
            )
            self.detailed_results['mobility'] = detailed
            self.indicators['mobility'] = mobility_stats
        
        return self.indicators
    
    def step_3_export_results(
        self,
        output_dir: Optional[str] = None,
        formats: list = ['csv', 'parquet', 'json']
    ) -> Dict[str, str]:
        """
        Étape 3: Export des résultats
        
        Args:
            output_dir: Répertoire de sortie
            formats: Formats d'export souhaités
            
        Returns:
            Dictionnaire avec les chemins des fichiers exportés
        """
        logger.info("=" * 50)
        logger.info("ÉTAPE 3: Export des résultats")
        logger.info("=" * 50)
        
        if output_dir is None:
            output_dir = self.config['paths']['processed_dir']
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        exported_files = {}
        
        # Export des datasets enrichis
        for name, df in self.datasets.items():
            if name.endswith('_enriched') or name in ['users', 'poverty', 'migration', 'mobility']:
                base_name = f"{name}_{timestamp}"
                
                if 'csv' in formats:
                    csv_path = output_path / f"{base_name}.csv"
                    df.to_csv(csv_path, index=False)
                    exported_files[f"{name}_csv"] = str(csv_path)
                
                if 'parquet' in formats:
                    parquet_path = output_path / f"{base_name}.parquet"
                    df.to_parquet(parquet_path, index=False)
                    exported_files[f"{name}_parquet"] = str(parquet_path)
        
        # Export des indicateurs
        if 'json' in formats:
            import json
            
            # Conversion des indicateurs pour JSON
            indicators_json = self._prepare_indicators_for_json(self.indicators)
            
            json_path = output_path / f"indicators_{timestamp}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(indicators_json, f, indent=2, ensure_ascii=False, default=str)
            exported_files['indicators_json'] = str(json_path)
        
        # Export du rapport de synthèse
        report_path = output_path / f"report_{timestamp}.yml"
        self._generate_report(report_path)
        exported_files['report'] = str(report_path)
        
        logger.info(f"✓ {len(exported_files)} fichiers exportés vers {output_path}")
        
        return exported_files
    
    def _prepare_indicators_for_json(self, indicators: Dict) -> Dict:
        """
        Prépare les indicateurs pour l'export JSON
        
        Convertit les types numpy et pandas en types Python natifs
        """
        import numpy as np
        
        def convert(obj):
            if isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(v) for v in obj]
            elif isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif pd.isna(obj):
                return None
            else:
                return obj
        
        return convert(indicators)
    
    def _generate_report(self, output_path: Path) -> None:
        """
        Génère un rapport de synthèse
        
        Args:
            output_path: Chemin du fichier de sortie
        """
        report = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'config_file': str(self.config_path),
                'version': self.config['project']['version']
            },
            'data_summary': {
                'n_users': len(self.datasets.get('users', [])),
                'n_poverty_records': len(self.datasets.get('poverty', [])),
                'n_migration_events': len(self.datasets.get('migration', [])),
                'n_mobility_trips': len(self.datasets.get('mobility', []))
            },
            'key_indicators': {}
        }
        
        # Indicateurs clés de pauvreté
        if 'poverty' in self.indicators:
            report['key_indicators']['poverty'] = {
                'poverty_rate': self.indicators['poverty'].get('poverty_rate'),
                'gini_coefficient': self.indicators['poverty'].get('gini_coefficient'),
                'mean_wealth_index': self.indicators['poverty'].get('mean_wealth_index')
            }
        
        # Indicateurs clés de migration
        if 'migration' in self.indicators:
            report['key_indicators']['migration'] = {
                'total_migrations': self.indicators['migration'].get('total_migrations'),
                'significant_migrations': self.indicators['migration'].get('significant_migrations'),
                'mean_distance_km': self.indicators['migration'].get('mean_distance_km')
            }
        
        # Indicateurs clés de mobilité
        if 'mobility' in self.indicators:
            report['key_indicators']['mobility'] = {
                'total_trips': self.indicators['mobility'].get('total_trips'),
                'avg_trip_distance_km': self.indicators['mobility'].get('avg_trip_distance_km'),
                'avg_trip_duration_min': self.indicators['mobility'].get('avg_trip_duration_min')
            }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(report, f, default_flow_style=False, allow_unicode=True)
    
    def run(self, save: bool = True) -> Dict:
        """
        Exécute le pipeline complet
        
        Args:
            save: Sauvegarder les résultats
            
        Returns:
            Dictionnaire avec tous les résultats
        """
        logger.info("=" * 60)
        logger.info("DÉMARRAGE DU PIPELINE COMPLET")
        logger.info(f"Projet: {self.config['project']['name']}")
        logger.info(f"Standard: {self.config['project']['standard']}")
        logger.info("=" * 60)
        
        start_time = datetime.now()
        
        # Étape 1: Génération
        self.step_1_generate_data(save=save)
        
        # Étape 2: Calcul des indicateurs
        self.step_2_calculate_indicators()
        
        # Étape 3: Export
        if save:
            exported = self.step_3_export_results()
        else:
            exported = {}
        
        # Durée totale
        duration = datetime.now() - start_time
        
        logger.info("=" * 60)
        logger.info(f"PIPELINE TERMINÉ en {duration.total_seconds():.1f} secondes")
        logger.info("=" * 60)
        
        return {
            'datasets': self.datasets,
            'indicators': self.indicators,
            'detailed_results': self.detailed_results,
            'exported_files': exported,
            'duration_seconds': duration.total_seconds()
        }


def main():
    """Point d'entrée principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Pipeline d'analyse des données de téléphonie mobile"
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config/data_params.yml',
        help='Chemin vers le fichier de configuration'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Ne pas sauvegarder les fichiers'
    )
    parser.add_argument(
        '--step',
        type=int,
        choices=[1, 2, 3],
        help='Exécuter une seule étape (1=génération, 2=indicateurs, 3=export)'
    )
    
    args = parser.parse_args()
    
    # Initialisation du pipeline
    pipeline = MobilityPipeline(config_path=args.config)
    
    # Exécution
    if args.step:
        if args.step == 1:
            pipeline.step_1_generate_data(save=not args.no_save)
        elif args.step == 2:
            # Charger les données existantes si disponibles
            pipeline.step_1_generate_data(save=False)
            pipeline.step_2_calculate_indicators()
        elif args.step == 3:
            pipeline.step_1_generate_data(save=False)
            pipeline.step_2_calculate_indicators()
            pipeline.step_3_export_results()
    else:
        results = pipeline.run(save=not args.no_save)
        
        # Affichage du résumé
        print("\n" + "=" * 50)
        print("RÉSUMÉ DU PIPELINE")
        print("=" * 50)
        print(f"Durée totale: {results['duration_seconds']:.1f} secondes")
        print(f"Datasets générés: {len(results['datasets'])}")
        print(f"Fichiers exportés: {len(results['exported_files'])}")
        
        if 'poverty' in results['indicators']:
            print(f"\nTaux de pauvreté: {results['indicators']['poverty'].get('poverty_rate', 'N/A'):.1%}")
        
        if 'migration' in results['indicators']:
            print(f"Migrations significatives: {results['indicators']['migration'].get('significant_migrations', 'N/A')}")
        
        if 'mobility' in results['indicators']:
            print(f"Total trajets: {results['indicators']['mobility'].get('total_trips', 'N/A')}")


if __name__ == "__main__":
    main()
