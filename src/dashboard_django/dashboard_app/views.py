"""
Vues du Dashboard Django
Rendu des templates HTML avec données du contexte
"""
from django.shortcuts import render
from django.views import View
from services.data_service import data_service


class DashboardMixin:
    """Mixin pour ajouter les données communes au contexte"""
    
    def get_base_context(self):
        """Retourne le contexte de base pour toutes les pages"""
        datasets = data_service.load_all_datasets()
        return {
            'datasets_loaded': {
                name: len(df) for name, df in datasets.items()
            },
            'current_page': '',
        }


class OverviewView(DashboardMixin, View):
    """Vue d'ensemble du dashboard"""
    template_name = 'dashboard/overview.html'
    
    def get(self, request):
        context = self.get_base_context()
        context['current_page'] = 'overview'
        context['stats'] = data_service.get_overview_stats()
        return render(request, self.template_name, context)


class PovertyView(DashboardMixin, View):
    """Vue d'analyse de la pauvreté"""
    template_name = 'dashboard/poverty.html'
    
    def get(self, request):
        context = self.get_base_context()
        context['current_page'] = 'poverty'
        context['stats'] = data_service.get_poverty_stats()
        return render(request, self.template_name, context)


class MigrationView(DashboardMixin, View):
    """Vue d'analyse des migrations"""
    template_name = 'dashboard/migration.html'
    
    def get(self, request):
        context = self.get_base_context()
        context['current_page'] = 'migration'
        context['stats'] = data_service.get_migration_stats()
        return render(request, self.template_name, context)


class MobilityView(DashboardMixin, View):
    """Vue d'analyse de la mobilité"""
    template_name = 'dashboard/mobility.html'
    
    def get(self, request):
        context = self.get_base_context()
        context['current_page'] = 'mobility'
        context['stats'] = data_service.get_mobility_stats()
        return render(request, self.template_name, context)


class MapView(DashboardMixin, View):
    """Vue cartographique"""
    template_name = 'dashboard/map.html'
    
    def get(self, request):
        context = self.get_base_context()
        context['current_page'] = 'map'
        context['map_data'] = data_service.get_map_data()
        return render(request, self.template_name, context)
