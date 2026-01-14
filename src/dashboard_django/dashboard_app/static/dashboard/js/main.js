/**
 * Dashboard CI Mobility - JavaScript principal
 * ANStat - DataLab
 */

// Configuration
const API_BASE_URL = '/api';

// Toggle sidebar
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }
    
    // Format des nombres
    formatNumbers();
});

// Formatter les nombres avec séparateurs
function formatNumbers() {
    document.querySelectorAll('[data-format="number"]').forEach(el => {
        const num = parseInt(el.textContent);
        if (!isNaN(num)) {
            el.textContent = num.toLocaleString('fr-FR');
        }
    });
}

// Rafraîchir les données
async function refreshData() {
    const btn = event.target;
    const originalText = btn.innerHTML;
    
    btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Chargement...';
    btn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            showToast('Données actualisées avec succès', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            throw new Error('Erreur lors du rafraîchissement');
        }
    } catch (error) {
        showToast('Erreur: ' + error.message, 'danger');
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// Récupérer un cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Afficher un toast
function showToast(message, type = 'info') {
    // Créer le conteneur s'il n'existe pas
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1100';
        document.body.appendChild(container);
    }
    
    // Créer le toast
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    container.appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

// Télécharger des données
async function downloadData(dataset) {
    try {
        const response = await fetch(`${API_BASE_URL}/dataset/${dataset}/?limit=100000`);
        const data = await response.json();
        
        if (data.data) {
            const csv = convertToCSV(data.data);
            downloadCSV(csv, `${dataset}_export.csv`);
            showToast(`Export de ${data.returned_rows} lignes réussi`, 'success');
        }
    } catch (error) {
        showToast('Erreur lors du téléchargement', 'danger');
    }
}

// Convertir en CSV
function convertToCSV(data) {
    if (!data || data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const rows = data.map(row => 
        headers.map(h => {
            let val = row[h];
            if (typeof val === 'string' && val.includes(',')) {
                val = `"${val}"`;
            }
            return val;
        }).join(',')
    );
    
    return [headers.join(','), ...rows].join('\n');
}

// Télécharger un fichier CSV
function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Utilitaires pour les graphiques
const chartColors = {
    primary: '#FF6B00',
    secondary: '#0d6efd',
    success: '#198754',
    warning: '#ffc107',
    danger: '#dc3545',
    info: '#0dcaf0',
    light: '#f8f9fa',
    dark: '#212529'
};

const chartPalette = [
    '#FF6B00', '#0d6efd', '#198754', '#ffc107', 
    '#dc3545', '#6c757d', '#0dcaf0', '#6610f2',
    '#fd7e14', '#20c997', '#e83e8c', '#17a2b8'
];

// Configuration par défaut pour Chart.js
Chart.defaults.font.family = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif";
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(0,0,0,0.8)';
Chart.defaults.plugins.tooltip.padding = 12;
Chart.defaults.plugins.tooltip.cornerRadius = 8;

// Formatter les axes
function formatAxis(value) {
    if (value >= 1000000) {
        return (value / 1000000).toFixed(1) + 'M';
    } else if (value >= 1000) {
        return (value / 1000).toFixed(1) + 'K';
    }
    return value;
}

// Exporter les fonctions globales
window.refreshData = refreshData;
window.downloadData = downloadData;
window.showToast = showToast;
window.chartColors = chartColors;
window.chartPalette = chartPalette;
