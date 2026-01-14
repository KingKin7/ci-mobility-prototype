"""
API REST pour le Dashboard CI Mobility
Fournit les données JSON pour le frontend
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from services.data_service import data_service


class OverviewAPIView(APIView):
    """API pour la vue d'ensemble"""
    
    def get(self, request):
        try:
            stats = data_service.get_overview_stats()
            return Response(stats)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PovertyAPIView(APIView):
    """API pour les statistiques de pauvreté"""
    
    def get(self, request):
        try:
            stats = data_service.get_poverty_stats()
            return Response(stats)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MigrationAPIView(APIView):
    """API pour les statistiques de migration"""
    
    def get(self, request):
        try:
            stats = data_service.get_migration_stats()
            return Response(stats)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MobilityAPIView(APIView):
    """API pour les statistiques de mobilité"""
    
    def get(self, request):
        try:
            stats = data_service.get_mobility_stats()
            return Response(stats)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MapAPIView(APIView):
    """API pour les données cartographiques"""
    
    def get(self, request):
        try:
            data = data_service.get_map_data()
            return Response(data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DatasetAPIView(APIView):
    """API pour télécharger les datasets bruts"""
    
    def get(self, request, dataset_name):
        try:
            df = data_service.get_dataset(dataset_name)
            if df is None:
                return Response(
                    {'error': f'Dataset {dataset_name} not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Limiter à 1000 lignes pour l'API
            limit = int(request.query_params.get('limit', 1000))
            data = df.head(limit).to_dict('records')
            
            return Response({
                'dataset': dataset_name,
                'total_rows': len(df),
                'returned_rows': len(data),
                'columns': df.columns.tolist(),
                'data': data
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RefreshAPIView(APIView):
    """API pour rafraîchir le cache des données"""
    
    def post(self, request):
        try:
            data_service.load_all_datasets(force_reload=True)
            return Response({'status': 'success', 'message': 'Data reloaded'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
