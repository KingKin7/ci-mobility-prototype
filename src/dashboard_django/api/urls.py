"""
URLs de l'API REST
"""
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('overview/', views.OverviewAPIView.as_view(), name='overview'),
    path('poverty/', views.PovertyAPIView.as_view(), name='poverty'),
    path('migration/', views.MigrationAPIView.as_view(), name='migration'),
    path('mobility/', views.MobilityAPIView.as_view(), name='mobility'),
    path('map/', views.MapAPIView.as_view(), name='map'),
    path('dataset/<str:dataset_name>/', views.DatasetAPIView.as_view(), name='dataset'),
    path('refresh/', views.RefreshAPIView.as_view(), name='refresh'),
]
