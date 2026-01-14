"""
URLs du Dashboard
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.OverviewView.as_view(), name='overview'),
    path('poverty/', views.PovertyView.as_view(), name='poverty'),
    path('migration/', views.MigrationView.as_view(), name='migration'),
    path('mobility/', views.MobilityView.as_view(), name='mobility'),
    path('map/', views.MapView.as_view(), name='map'),
]
