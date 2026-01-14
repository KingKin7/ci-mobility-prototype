"""
Dashboard interactif - Mobilité Côte d'Ivoire
Projet ANStat - Analyse des données de téléphonie mobile

Lancer avec: streamlit run src/dashboard/app.py
"""

import sys
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Mobilité CI",
    page_icon="🇨🇮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DICTIONNAIRES DE TRADUCTION
# ============================================================

# Traduction des types de migration
MIGRATION_TYPE_FR = {
    "work_migration": "Migration travail",
    "seasonal_agriculture": "Agriculture saisonnière",
    "permanent_relocation": "Relocalisation permanente",
    "permanent_relacoation": "Relocalisation permanente",  # Typo dans les données
    "education_migration": "Migration études",
    "circular_migration": "Migration circulaire",
    "return_migration": "Migration retour",
    "family_migration": "Migration familiale",
}

# Traduction des modes de transport
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

# Traduction des colonnes de pauvreté
POVERTY_COLS_FR = {
    "recharge_amount_fcfa": "Montant recharge (FCFA)",
    "mobility_radius_km": "Rayon mobilité (km)",
    "contact_diversity_score": "Score diversité contacts",
    "call_duration_sec": "Durée appel (sec)",
    "data_mb": "Données (Mo)",
    "recharge_frequency_weekly": "Fréquence recharge hebdo",
    "wealth_index": "Indice de richesse",
    "user_id": "ID utilisateur",
}

# Traduction des motifs de déplacement
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


def translate_column(
    df: pd.DataFrame, column: str, translation_dict: Dict
) -> pd.DataFrame:
    """Traduit les valeurs d'une colonne selon un dictionnaire"""
    if column in df.columns:
        df = df.copy()
        df[column] = df[column].map(lambda x: translation_dict.get(x, x))
    return df


def translate_dataframe_columns(
    df: pd.DataFrame, translation_dict: Dict
) -> pd.DataFrame:
    """Traduit les noms de colonnes d'un DataFrame"""
    df = df.copy()
    df.columns = [translation_dict.get(col, col) for col in df.columns]
    return df


# Styles CSS personnalisés
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B00;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    """Charge les données les plus récentes"""
    data_dir = Path("data/synthetic")

    if not data_dir.exists():
        return {}

    datasets = {}

    for dataset_name in ["users", "poverty", "migration", "mobility"]:
        files = list(data_dir.glob(f"{dataset_name}_*.csv"))
        if files:
            latest_file = max(files, key=lambda x: x.stat().st_mtime)
            datasets[dataset_name] = pd.read_csv(latest_file)

    return datasets


@st.cache_data
def calculate_wealth_index(poverty_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule l'indice de richesse à partir des données de pauvreté
    Utilise les colonnes disponibles dans poverty_df
    """
    if poverty_df.empty:
        return pd.DataFrame()

    # Colonnes utilisées pour calculer l'indice de richesse
    feature_cols = []
    potential_features = [
        "recharge_amount_fcfa",
        "recharge_frequency_weekly",
        "call_duration_sec",
        "data_mb",
        "contact_diversity_score",
        "mobility_radius_km",
    ]

    for col in potential_features:
        if col in poverty_df.columns:
            feature_cols.append(col)

    if not feature_cols:
        st.warning("Aucune colonne de feature disponible pour calculer l'indice")
        return pd.DataFrame()

    # Agrégation par utilisateur (moyenne sur la période)
    agg_dict = {col: "mean" for col in feature_cols}

    # Ajouter les colonnes de localisation si présentes
    location_cols = ["locality", "department", "region", "latitude", "longitude"]
    for loc_col in location_cols:
        if loc_col in poverty_df.columns:
            agg_dict[loc_col] = "first"

    user_stats = poverty_df.groupby("user_id").agg(agg_dict).reset_index()

    # Normalisation min-max pour chaque feature
    for col in feature_cols:
        col_min = user_stats[col].min()
        col_max = user_stats[col].max()
        if col_max > col_min:
            user_stats[f"{col}_norm"] = (user_stats[col] - col_min) / (
                col_max - col_min
            )
        else:
            user_stats[f"{col}_norm"] = 0.5

    # Score de richesse = moyenne des features normalisées
    norm_cols = [f"{col}_norm" for col in feature_cols]
    user_stats["wealth_index"] = user_stats[norm_cols].mean(axis=1)

    # Quintiles de richesse
    user_stats["wealth_quintile"] = pd.qcut(
        user_stats["wealth_index"],
        q=5,
        labels=["Q1_Très pauvre", "Q2_Pauvre", "Q3_Moyen", "Q4_Aisé", "Q5_Riche"],
    )

    # Classification pauvre/non-pauvre (Q1 et Q2 = pauvres)
    user_stats["is_poor"] = user_stats["wealth_quintile"].isin(
        ["Q1_Très pauvre", "Q2_Pauvre"]
    )

    # Supprimer les colonnes normalisées intermédiaires
    user_stats = user_stats.drop(columns=norm_cols)

    return user_stats


def show_overview(data: Dict):
    """Page d'accueil avec vue d'ensemble"""
    st.markdown(
        '<h1 class="main-header">🇨🇮 Dashboard Mobilité Côte d\'Ivoire</h1>',
        unsafe_allow_html=True,
    )

    st.markdown("### 📊 Vue d'ensemble du projet")

    users_df = data.get("users", pd.DataFrame())
    poverty_df = data.get("poverty", pd.DataFrame())
    migration_df = data.get("migration", pd.DataFrame())
    mobility_df = data.get("mobility", pd.DataFrame())

    # Calculer les indicateurs de pauvreté
    if not poverty_df.empty:
        poverty_stats = calculate_wealth_index(poverty_df)
        if not poverty_stats.empty and "is_poor" in poverty_stats.columns:
            poverty_rate = poverty_stats["is_poor"].mean()
        else:
            poverty_rate = 0.4
    else:
        poverty_rate = 0
        poverty_stats = pd.DataFrame()

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="👥 Utilisateurs", value=f"{len(users_df):,}", delta="Profils générés"
        )

    with col2:
        st.metric(
            label="📉 Taux de pauvreté", value=f"{poverty_rate:.1%}", delta="Q1 + Q2"
        )

    with col3:
        st.metric(
            label="🚶 Migrations",
            value=f"{len(migration_df):,}",
            delta="Événements détectés",
        )

    with col4:
        st.metric(
            label="🚗 Trajets",
            value=f"{len(mobility_df):,}",
            delta="Déplacements analysés",
        )

    st.markdown("---")

    # Distribution géographique
    st.markdown("### 🗺️ Distribution géographique des utilisateurs")

    if not users_df.empty and "locality" in users_df.columns:
        col1, col2 = st.columns([2, 1])

        with col1:
            locality_counts = users_df["locality"].value_counts().head(15)
            fig = px.bar(
                x=locality_counts.values,
                y=locality_counts.index,
                orientation="h",
                title="Top 15 des localités par nombre d'utilisateurs",
                labels={"x": "Nombre d'utilisateurs", "y": "Localité"},
                color=locality_counts.values,
                color_continuous_scale="Oranges",
            )
            fig.update_layout(showlegend=False, height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 📍 Répartition")
            if "urban_rural" in users_df.columns:
                urban_pct = (users_df["urban_rural"] == "urban").mean() * 100
                st.metric("Zone urbaine", f"{urban_pct:.1f}%")
                st.metric("Zone rurale", f"{100-urban_pct:.1f}%")

            st.markdown("#### 📱 Types de téléphone")
            if "phone_type" in users_df.columns:
                phone_dist = users_df["phone_type"].value_counts(normalize=True) * 100
                for phone, pct in phone_dist.items():
                    st.write(f"- {phone}: {pct:.1f}%")

    # Résumé par région
    st.markdown("### 🏛️ Résumé par région")

    if not users_df.empty and "region" in users_df.columns:
        region_summary = (
            users_df.groupby("region")
            .agg(
                {
                    "user_id": "count",
                }
            )
            .reset_index()
        )
        region_summary.columns = ["Région", "Nb utilisateurs"]
        region_summary = region_summary.sort_values("Nb utilisateurs", ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.pie(
                region_summary,
                values="Nb utilisateurs",
                names="Région",
                title="Répartition par région",
                color_discrete_sequence=px.colors.qualitative.Set3,
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.dataframe(
                region_summary.round(1), use_container_width=True, hide_index=True
            )


def show_poverty_analysis(data: Dict):
    """Page d'analyse de la pauvreté"""
    st.markdown("## 📉 Analyse de la Pauvreté")

    poverty_df = data.get("poverty", pd.DataFrame())

    if poverty_df.empty:
        st.warning("Aucune donnée de pauvreté disponible")
        return

    # Calculer les indicateurs de richesse
    poverty_stats = calculate_wealth_index(poverty_df)

    if poverty_stats.empty:
        st.error("Impossible de calculer les indicateurs de pauvreté")
        return

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Vue d'ensemble", "🗺️ Carte", "📋 Détails"])

    with tab1:
        show_poverty_overview(poverty_stats)

    with tab2:
        show_poverty_map(poverty_stats)

    with tab3:
        show_poverty_details(poverty_stats)


def show_poverty_overview(poverty_stats: pd.DataFrame):
    """Affiche la vue d'ensemble de la pauvreté"""

    # Métriques
    col1, col2, col3, col4 = st.columns(4)

    poverty_rate = (
        poverty_stats["is_poor"].mean() if "is_poor" in poverty_stats.columns else 0
    )

    with col1:
        st.metric("Taux de pauvreté", f"{poverty_rate:.1%}")
    with col2:
        avg_recharge = (
            poverty_stats["recharge_amount_fcfa"].mean()
            if "recharge_amount_fcfa" in poverty_stats.columns
            else 0
        )
        st.metric("Recharge moyenne", f"{avg_recharge:,.0f} FCFA")
    with col3:
        avg_mobility = (
            poverty_stats["mobility_radius_km"].mean()
            if "mobility_radius_km" in poverty_stats.columns
            else 0
        )
        st.metric("Mobilité moyenne", f"{avg_mobility:.1f} km")
    with col4:
        avg_diversity = (
            poverty_stats["contact_diversity_score"].mean()
            if "contact_diversity_score" in poverty_stats.columns
            else 0
        )
        st.metric("Diversité contacts", f"{avg_diversity:.2f}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        # Distribution des quintiles
        if "wealth_quintile" in poverty_stats.columns:
            quintile_counts = (
                poverty_stats["wealth_quintile"].value_counts().sort_index()
            )

            colors = ["#d73027", "#fc8d59", "#fee08b", "#d9ef8b", "#1a9850"]

            fig = px.bar(
                x=quintile_counts.index.astype(str),
                y=quintile_counts.values,
                title="Distribution par quintile de richesse",
                labels={"x": "Quintile", "y": "Nombre d'utilisateurs"},
                color=quintile_counts.index.astype(str),
                color_discrete_sequence=colors,
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Corrélation richesse vs mobilité
        if (
            "mobility_radius_km" in poverty_stats.columns
            and "recharge_amount_fcfa" in poverty_stats.columns
        ):
            sample_size = min(1000, len(poverty_stats))
            sample_df = poverty_stats.sample(n=sample_size, random_state=42)

            fig = px.scatter(
                sample_df,
                x="mobility_radius_km",
                y="recharge_amount_fcfa",
                color="wealth_index" if "wealth_index" in sample_df.columns else None,
                title="Corrélation Mobilité vs Recharges",
                labels={
                    "mobility_radius_km": "Rayon de mobilité (km)",
                    "recharge_amount_fcfa": "Montant recharges (FCFA)",
                    "wealth_index": "Indice de richesse",
                },
                color_continuous_scale="RdYlGn",
            )
            st.plotly_chart(fig, use_container_width=True)

    # Distribution de l'indice de richesse
    if "wealth_index" in poverty_stats.columns:
        st.markdown("### 📈 Distribution de l'indice de richesse")
        fig = px.histogram(
            poverty_stats,
            x="wealth_index",
            nbins=50,
            title="Distribution de l'indice de richesse (0 = pauvre, 1 = riche)",
            labels={"wealth_index": "Indice de richesse", "count": "Nombre"},
            color_discrete_sequence=["#FF6B00"],
        )
        median_val = poverty_stats["wealth_index"].median()
        fig.add_vline(
            x=median_val,
            line_dash="dash",
            annotation_text=f"Médiane: {median_val:.2f}",
            line_color="red",
        )
        st.plotly_chart(fig, use_container_width=True)


def show_poverty_map(poverty_stats: pd.DataFrame):
    """Affiche la carte de pauvreté par région"""
    st.subheader("🗺️ Carte de la pauvreté par région")

    # Vérifier que la colonne region existe
    if "region" not in poverty_stats.columns:
        st.warning("⚠️ La colonne 'region' n'est pas disponible dans les données.")
        return

    if "wealth_index" not in poverty_stats.columns:
        st.warning("⚠️ L'indice de richesse n'a pas pu être calculé.")
        return

    # Agrégation par région
    regional_stats = (
        poverty_stats.groupby("region")
        .agg({"wealth_index": ["mean", "std"], "user_id": "count", "is_poor": "mean"})
        .reset_index()
    )

    regional_stats.columns = [
        "Région",
        "Indice moyen",
        "Écart-type",
        "Population",
        "Taux pauvreté",
    ]
    regional_stats["Taux pauvreté (%)"] = regional_stats["Taux pauvreté"] * 100
    regional_stats = regional_stats.sort_values("Indice moyen")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Graphique en barres par région
        fig = px.bar(
            regional_stats,
            x="Région",
            y="Indice moyen",
            color="Taux pauvreté (%)",
            title="Indice de richesse moyen par région",
            labels={"Indice moyen": "Indice de richesse (0-1)"},
            color_continuous_scale="RdYlGn_r",  # Rouge = pauvre, Vert = riche
        )
        fig.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Statistiques régionales")
        display_df = regional_stats[
            ["Région", "Indice moyen", "Taux pauvreté (%)", "Population"]
        ].copy()
        display_df["Indice moyen"] = display_df["Indice moyen"].round(3)
        display_df["Taux pauvreté (%)"] = display_df["Taux pauvreté (%)"].round(1)
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)

    # Carte géographique si coordonnées disponibles
    if "latitude" in poverty_stats.columns and "longitude" in poverty_stats.columns:
        st.markdown("#### 🌍 Carte interactive")

        # Centroïdes par région
        region_coords = (
            poverty_stats.groupby("region")
            .agg(
                {
                    "latitude": "mean",
                    "longitude": "mean",
                    "wealth_index": "mean",
                    "user_id": "count",
                }
            )
            .reset_index()
        )

        fig = px.scatter_mapbox(
            region_coords,
            lat="latitude",
            lon="longitude",
            size="user_id",
            color="wealth_index",
            hover_name="region",
            hover_data={
                "wealth_index": ":.3f",
                "user_id": True,
                "latitude": False,
                "longitude": False,
            },
            color_continuous_scale="RdYlGn",
            mapbox_style="carto-positron",
            center={"lat": 7.54, "lon": -5.55},
            zoom=5.5,
            title="Indice de richesse par région (taille = population)",
            size_max=50,
        )
        fig.update_layout(height=500, margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True, key="poverty_map_scatter")

    # Classement des régions
    st.markdown("#### 🏆 Classement des régions")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🔴 Régions les plus pauvres**")
        poorest = regional_stats.nsmallest(5, "Indice moyen")[
            ["Région", "Indice moyen", "Taux pauvreté (%)"]
        ]
        st.dataframe(poorest, hide_index=True)

    with col2:
        st.markdown("**🟢 Régions les plus riches**")
        richest = regional_stats.nlargest(5, "Indice moyen")[
            ["Région", "Indice moyen", "Taux pauvreté (%)"]
        ]
        st.dataframe(richest, hide_index=True)


def show_poverty_details(poverty_stats: pd.DataFrame):
    """Affiche les détails et permet l'export"""
    st.subheader("📋 Détails des indicateurs")

    # Statistiques descriptives
    st.markdown("#### 📈 Statistiques descriptives")

    numeric_cols = [
        "wealth_index",
        "recharge_amount_fcfa",
        "mobility_radius_km",
        "contact_diversity_score",
        "call_duration_sec",
        "data_mb",
    ]
    available_cols = [col for col in numeric_cols if col in poverty_stats.columns]

    if available_cols:
        desc_stats = poverty_stats[available_cols].describe().T
        desc_stats = desc_stats.round(3)
        # Traduire les noms de colonnes
        desc_stats.index = [POVERTY_COLS_FR.get(col, col) for col in desc_stats.index]
        st.dataframe(desc_stats, use_container_width=True)

    # Caractéristiques par quintile
    if "wealth_quintile" in poverty_stats.columns:
        st.markdown("#### 📊 Caractéristiques moyennes par quintile")

        agg_cols = {col: "mean" for col in available_cols if col != "wealth_index"}
        agg_cols["user_id"] = "count"

        quintile_stats = poverty_stats.groupby("wealth_quintile").agg(agg_cols).round(2)
        quintile_stats = quintile_stats.rename(columns={"user_id": "Effectif"})

        # Traduire les noms de colonnes
        quintile_stats.columns = [
            POVERTY_COLS_FR.get(col, col) for col in quintile_stats.columns
        ]

        st.dataframe(quintile_stats, use_container_width=True)

    # Export des données
    st.markdown("#### 💾 Export des données")

    csv = poverty_stats.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger les données (CSV)",
        data=csv,
        file_name="analyse_pauvrete_resultats.csv",
        mime="text/csv",
    )


def show_migration_analysis(data: Dict):
    """Page d'analyse des migrations"""
    st.markdown("## 🚶 Analyse des Migrations")

    migration_df = data.get("migration", pd.DataFrame())

    if migration_df.empty:
        st.warning("Aucune donnée de migration disponible")
        return

    # Traduire les types de migration pour l'affichage
    migration_df_display = translate_column(
        migration_df.copy(), "movement_type", MIGRATION_TYPE_FR
    )

    # Métriques
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total migrations", f"{len(migration_df):,}")
    with col2:
        st.metric("Distance moyenne", f"{migration_df['distance_km'].mean():.1f} km")
    with col3:
        st.metric(
            "Durée moyenne séjour",
            f"{migration_df['residence_duration_days'].mean():.0f} jours",
        )
    with col4:
        return_rate = migration_df["is_return_migration"].mean()
        st.metric("Taux retour", f"{return_rate:.1%}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if "movement_type" in migration_df_display.columns:
            type_counts = migration_df_display["movement_type"].value_counts()
            fig = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                title="Types de migration",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            migration_df,
            x="distance_km",
            nbins=30,
            title="Distribution des distances de migration",
            labels={"distance_km": "Distance (km)", "count": "Nombre"},
            color_discrete_sequence=["#FF6B00"],
        )
        st.plotly_chart(fig, use_container_width=True)

    # Flux migratoires
    st.markdown("### 🔄 Flux migratoires principaux")

    if (
        "origin_locality" in migration_df.columns
        and "current_locality" in migration_df.columns
    ):
        flows = (
            migration_df.groupby(["origin_locality", "current_locality"])
            .size()
            .reset_index(name="count")
        )
        flows = flows.sort_values("count", ascending=False).head(15)

        fig = px.bar(
            flows,
            x="count",
            y=flows.apply(
                lambda x: f"{x['origin_locality']} → {x['current_locality']}", axis=1
            ),
            orientation="h",
            title="Top 15 des corridors migratoires",
            labels={"count": "Nombre de migrations", "y": "Corridor"},
            color="count",
            color_continuous_scale="Oranges",
        )
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Matrice O-D
    st.markdown("### 📊 Matrice Origine-Destination")

    if (
        "origin_region" in migration_df.columns
        and "current_region" in migration_df.columns
    ):
        od_matrix = pd.crosstab(
            migration_df["origin_region"], migration_df["current_region"]
        )

        fig = px.imshow(
            od_matrix,
            labels=dict(
                x="Région de destination", y="Région d'origine", color="Migrations"
            ),
            title="Flux migratoires par région",
            color_continuous_scale="YlOrRd",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Statistiques par type de migration
    st.markdown("### 📊 Statistiques par type de migration")

    if "movement_type" in migration_df.columns:
        type_stats = (
            migration_df.groupby("movement_type")
            .agg(
                {
                    "distance_km": ["mean", "median"],
                    "residence_duration_days": "mean",
                    "user_id": "count",
                }
            )
            .round(1)
        )
        type_stats.columns = [
            "Distance moy. (km)",
            "Distance méd. (km)",
            "Durée moy. (jours)",
            "Effectif",
        ]
        # Traduire l'index
        type_stats.index = [MIGRATION_TYPE_FR.get(idx, idx) for idx in type_stats.index]
        st.dataframe(type_stats, use_container_width=True)


def show_mobility_analysis(data: Dict):
    """Page d'analyse de la mobilité quotidienne"""
    st.markdown("## 🚗 Analyse de la Mobilité Quotidienne")

    mobility_df = data.get("mobility", pd.DataFrame())

    if mobility_df.empty:
        st.warning("Aucune donnée de mobilité disponible")
        return

    # Tabs pour organiser les analyses
    tab1, tab2, tab3 = st.tabs(["📊 Vue d'ensemble", "🚦 Congestion", "📈 Détails"])

    with tab1:
        show_mobility_overview(mobility_df)

    with tab2:
        show_congestion_analysis(mobility_df)

    with tab3:
        show_mobility_details(mobility_df)


def show_mobility_overview(mobility_df: pd.DataFrame):
    """Vue d'ensemble de la mobilité"""

    # Traduire les modes de transport pour l'affichage
    mobility_df_display = translate_column(
        mobility_df.copy(), "transport_mode", TRANSPORT_MODE_FR
    )
    mobility_df_display = translate_column(
        mobility_df_display, "trip_purpose", TRIP_PURPOSE_FR
    )

    # Métriques
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total trajets", f"{len(mobility_df):,}")
    with col2:
        st.metric("Distance moyenne", f"{mobility_df['distance_km'].mean():.2f} km")
    with col3:
        st.metric("Durée moyenne", f"{mobility_df['duration_min'].mean():.1f} min")
    with col4:
        st.metric("Vitesse moyenne", f"{mobility_df['speed_kmh'].mean():.1f} km/h")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if "transport_mode" in mobility_df_display.columns:
            mode_counts = mobility_df_display["transport_mode"].value_counts()
            fig = px.pie(
                values=mode_counts.values,
                names=mode_counts.index,
                title="Répartition modale des déplacements",
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        if "trip_purpose" in mobility_df_display.columns:
            purpose_counts = mobility_df_display["trip_purpose"].value_counts()
            fig = px.bar(
                x=purpose_counts.index,
                y=purpose_counts.values,
                title="Motifs de déplacement",
                labels={"x": "Motif", "y": "Nombre de trajets"},
                color=purpose_counts.values,
                color_continuous_scale="Viridis",
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


def show_congestion_analysis(mobility_df: pd.DataFrame):
    """Analyse de la congestion par zone et heure"""

    st.subheader("🚦 Analyse de la Congestion")

    # Calcul de l'indice de congestion
    # Congestion = temps réel / temps théorique (basé sur la vitesse libre)
    # Plus la vitesse est basse, plus la congestion est élevée

    if "hour_of_day" not in mobility_df.columns:
        st.warning("Données horaires non disponibles")
        return

    # Vitesse de référence (flux libre) par mode
    free_flow_speeds = {
        "walking": 5,
        "bicycle": 15,
        "bus": 35,
        "taxi": 45,
        "motorbike": 40,
        "personal_car": 50,
    }

    # Calculer l'indice de congestion
    mobility_df = mobility_df.copy()
    mobility_df["free_flow_speed"] = (
        mobility_df["transport_mode"].map(free_flow_speeds).fillna(30)
    )
    mobility_df["congestion_index"] = mobility_df["free_flow_speed"] / mobility_df[
        "speed_kmh"
    ].clip(lower=1)
    mobility_df["congestion_index"] = mobility_df["congestion_index"].clip(
        upper=5
    )  # Limiter à 5x

    # ===== HEURES DE POINTE =====
    st.markdown("### ⏰ Heures de Pointe")

    hourly_stats = (
        mobility_df.groupby("hour_of_day")
        .agg(
            {
                "trip_id": "count",
                "speed_kmh": "mean",
                "congestion_index": "mean",
                "duration_min": "mean",
            }
        )
        .reset_index()
    )
    hourly_stats.columns = [
        "Heure",
        "Nb trajets",
        "Vitesse moy.",
        "Indice congestion",
        "Durée moy.",
    ]

    # Identifier les heures de pointe (top 4 heures avec le plus de trajets)
    peak_hours = hourly_stats.nlargest(4, "Nb trajets")["Heure"].tolist()

    col1, col2 = st.columns([2, 1])

    with col1:
        # Graphique combiné : trajets + congestion
        fig = go.Figure()

        # Barres pour le nombre de trajets
        colors = [
            "#FF6B00" if h in peak_hours else "#FFA500" for h in hourly_stats["Heure"]
        ]
        fig.add_trace(
            go.Bar(
                x=hourly_stats["Heure"],
                y=hourly_stats["Nb trajets"],
                name="Nombre de trajets",
                marker_color=colors,
                yaxis="y",
            )
        )

        # Ligne pour l'indice de congestion
        fig.add_trace(
            go.Scatter(
                x=hourly_stats["Heure"],
                y=hourly_stats["Indice congestion"],
                name="Indice de congestion",
                mode="lines+markers",
                line=dict(color="#d62728", width=3),
                yaxis="y2",
            )
        )

        fig.update_layout(
            title="Distribution horaire des trajets et congestion",
            xaxis_title="Heure de la journée",
            yaxis=dict(title="Nombre de trajets", side="left"),
            yaxis2=dict(title="Indice de congestion", side="right", overlaying="y"),
            legend=dict(x=0.7, y=1.1, orientation="h"),
            hovermode="x unified",
        )

        # Ajouter des zones pour les heures de pointe
        fig.add_vrect(
            x0=6.5,
            x1=9.5,
            fillcolor="red",
            opacity=0.1,
            annotation_text="Pointe matin",
            annotation_position="top left",
        )
        fig.add_vrect(
            x0=16.5,
            x1=19.5,
            fillcolor="red",
            opacity=0.1,
            annotation_text="Pointe soir",
            annotation_position="top left",
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 🔴 Heures de pointe identifiées")

        # Pointe du matin
        morning_peak = hourly_stats[
            (hourly_stats["Heure"] >= 6) & (hourly_stats["Heure"] <= 10)
        ]
        if not morning_peak.empty:
            peak_morning_hour = morning_peak.loc[
                morning_peak["Nb trajets"].idxmax(), "Heure"
            ]
            st.metric("🌅 Pointe matin", f"{int(peak_morning_hour)}h00")

        # Pointe du soir
        evening_peak = hourly_stats[
            (hourly_stats["Heure"] >= 16) & (hourly_stats["Heure"] <= 20)
        ]
        if not evening_peak.empty:
            peak_evening_hour = evening_peak.loc[
                evening_peak["Nb trajets"].idxmax(), "Heure"
            ]
            st.metric("🌆 Pointe soir", f"{int(peak_evening_hour)}h00")

        # Heure la plus congestionnée
        most_congested = hourly_stats.loc[hourly_stats["Indice congestion"].idxmax()]
        st.metric(
            "🚨 Plus congestionnée",
            f"{int(most_congested['Heure'])}h00",
            delta=f"Indice: {most_congested['Indice congestion']:.2f}",
        )

        # Heure la plus fluide
        least_congested = hourly_stats.loc[hourly_stats["Indice congestion"].idxmin()]
        st.metric(
            "✅ Plus fluide",
            f"{int(least_congested['Heure'])}h00",
            delta=f"Indice: {least_congested['Indice congestion']:.2f}",
        )

    st.markdown("---")

    # ===== CONGESTION PAR ZONE =====
    st.markdown("### 🗺️ Congestion par Zone")

    if "locality" in mobility_df.columns:
        zone_stats = (
            mobility_df.groupby("locality")
            .agg(
                {
                    "trip_id": "count",
                    "speed_kmh": "mean",
                    "congestion_index": "mean",
                    "duration_min": "mean",
                    "distance_km": "mean",
                }
            )
            .reset_index()
        )
        zone_stats.columns = [
            "Localité",
            "Nb trajets",
            "Vitesse moy.",
            "Indice congestion",
            "Durée moy.",
            "Distance moy.",
        ]
        zone_stats = zone_stats.sort_values("Indice congestion", ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🔴 Zones les plus congestionnées")
            top_congested = zone_stats.head(10)

            fig = px.bar(
                top_congested,
                x="Indice congestion",
                y="Localité",
                orientation="h",
                title="Top 10 des zones les plus congestionnées",
                color="Indice congestion",
                color_continuous_scale="Reds",
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 🟢 Zones les plus fluides")
            least_congested_zones = zone_stats.tail(10).sort_values("Indice congestion")

            fig = px.bar(
                least_congested_zones,
                x="Indice congestion",
                y="Localité",
                orientation="h",
                title="Top 10 des zones les plus fluides",
                color="Indice congestion",
                color_continuous_scale="Greens_r",
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Tableau récapitulatif
        st.markdown("#### 📊 Tableau récapitulatif par zone")
        display_df = zone_stats.copy()
        display_df["Vitesse moy."] = (
            display_df["Vitesse moy."].round(1).astype(str) + " km/h"
        )
        display_df["Indice congestion"] = display_df["Indice congestion"].round(2)
        display_df["Durée moy."] = (
            display_df["Durée moy."].round(1).astype(str) + " min"
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ===== HEATMAP HEURE x ZONE =====
    st.markdown("### 🔥 Heatmap Congestion (Heure × Zone)")

    if "locality" in mobility_df.columns:
        # Sélectionner les top 15 zones par nombre de trajets
        top_zones = mobility_df["locality"].value_counts().head(15).index.tolist()
        filtered_df = mobility_df[mobility_df["locality"].isin(top_zones)]

        # Créer la matrice heure x zone
        heatmap_data = filtered_df.pivot_table(
            values="congestion_index",
            index="locality",
            columns="hour_of_day",
            aggfunc="mean",
        ).fillna(1)

        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Heure", y="Localité", color="Indice de congestion"),
            title="Congestion par heure et par zone (Top 15 zones)",
            color_continuous_scale="RdYlGn_r",
            aspect="auto",
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.info(
            "💡 **Lecture** : Plus la couleur est rouge, plus la zone est congestionnée à cette heure. Vert = fluide."
        )


def show_mobility_details(mobility_df: pd.DataFrame):
    """Détails et statistiques par mode de transport"""

    # Traduire les modes de transport pour l'affichage
    mobility_df_display = translate_column(
        mobility_df.copy(), "transport_mode", TRANSPORT_MODE_FR
    )

    st.subheader("📈 Statistiques détaillées")

    # Patterns horaires
    st.markdown("### ⏰ Patterns temporels")

    if "hour_of_day" in mobility_df.columns:
        hourly = (
            mobility_df.groupby("hour_of_day")
            .agg({"trip_id": "count", "distance_km": "mean", "duration_min": "mean"})
            .reset_index()
        )
        hourly.columns = [
            "Heure",
            "Nombre de trajets",
            "Distance moyenne",
            "Durée moyenne",
        ]

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=hourly["Heure"],
                y=hourly["Nombre de trajets"],
                name="Trajets",
                marker_color="#FF6B00",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=hourly["Heure"],
                y=hourly["Durée moyenne"] * 50,
                name="Durée moyenne (×50)",
                mode="lines+markers",
                line=dict(color="#2E86AB", width=3),
            )
        )
        fig.update_layout(
            title="Distribution horaire des déplacements",
            xaxis_title="Heure de la journée",
            yaxis_title="Nombre de trajets",
            legend=dict(x=0.7, y=1),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Statistiques par mode
    st.markdown("### 🚌 Statistiques par mode de transport")

    if "transport_mode" in mobility_df_display.columns:
        mode_stats = (
            mobility_df_display.groupby("transport_mode")
            .agg(
                {
                    "distance_km": ["mean", "sum"],
                    "duration_min": "mean",
                    "speed_kmh": "mean",
                    "trip_id": "count",
                }
            )
            .round(2)
        )
        mode_stats.columns = [
            "Distance moy. (km)",
            "Distance totale (km)",
            "Durée moy. (min)",
            "Vitesse moy. (km/h)",
            "Nb trajets",
        ]
        mode_stats = mode_stats.sort_values("Nb trajets", ascending=False)
        st.dataframe(mode_stats, use_container_width=True)

    # Export
    st.markdown("### 💾 Export des données")
    csv = mobility_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger les données de mobilité (CSV)",
        data=csv,
        file_name="donnees_mobilite.csv",
        mime="text/csv",
    )


def show_interactive_map(data: Dict):
    """Page avec carte interactive générale"""
    st.markdown("## 🗺️ Carte Interactive")

    users_df = data.get("users", pd.DataFrame())

    if users_df.empty or "home_lat" not in users_df.columns:
        st.warning("Aucune donnée géographique disponible")
        return

    viz_type = st.selectbox(
        "Type de visualisation",
        ["Densité par localité", "Carte de chaleur", "Points individuels"],
    )

    if viz_type == "Densité par localité":
        if "locality" in users_df.columns:
            locality_agg = (
                users_df.groupby("locality")
                .agg({"home_lat": "mean", "home_lon": "mean", "user_id": "count"})
                .reset_index()
            )

            fig = px.scatter_mapbox(
                locality_agg,
                lat="home_lat",
                lon="home_lon",
                size="user_id",
                hover_name="locality",
                color="user_id",
                color_continuous_scale="Oranges",
                mapbox_style="carto-positron",
                center={"lat": 7.54, "lon": -5.55},
                zoom=5.5,
                title="Densité d'utilisateurs par localité",
                size_max=50,
            )
            fig.update_layout(height=600, margin={"r": 0, "t": 30, "l": 0, "b": 0})
            st.plotly_chart(fig, use_container_width=True)

    elif viz_type == "Carte de chaleur":
        sample = users_df.sample(min(2000, len(users_df)))

        fig = px.density_mapbox(
            sample,
            lat="home_lat",
            lon="home_lon",
            radius=10,
            mapbox_style="carto-positron",
            center={"lat": 7.54, "lon": -5.55},
            zoom=5.5,
            title="Carte de chaleur de la densité de population",
        )
        fig.update_layout(height=600, margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

    else:
        sample = users_df.sample(min(500, len(users_df)))

        fig = px.scatter_mapbox(
            sample,
            lat="home_lat",
            lon="home_lon",
            hover_data=["locality"] if "locality" in sample.columns else None,
            mapbox_style="carto-positron",
            center={"lat": 7.54, "lon": -5.55},
            zoom=5.5,
            title="Échantillon d'utilisateurs",
        )
        fig.update_traces(marker=dict(size=5, color="#FF6B00"))
        fig.update_layout(height=600, margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

    # Statistiques
    st.markdown("### 📍 Statistiques géographiques")

    col1, col2, col3 = st.columns(3)

    with col1:
        if "locality" in users_df.columns:
            st.metric("Nombre de localités", users_df["locality"].nunique())
    with col2:
        if "region" in users_df.columns:
            st.metric("Nombre de régions", users_df["region"].nunique())
    with col3:
        if "department" in users_df.columns:
            st.metric("Nombre de départements", users_df["department"].nunique())


def main():
    """Application principale"""

    st.sidebar.title("🇨🇮 Navigation")

    # Charger les données
    with st.spinner("Chargement des données..."):
        data = load_data()

    if not data:
        st.error("❌ Aucune donnée trouvée dans data/synthetic/")
        st.info("Exécutez d'abord le pipeline pour générer les données:")
        st.code("python -m src.pipeline.run_pipeline")
        return

    # Afficher les données chargées
    st.sidebar.markdown("### 📊 Données chargées")
    for name, df in data.items():
        st.sidebar.success(f"✓ {name}: {len(df):,} lignes")

    st.sidebar.markdown("---")

    # Navigation
    page = st.sidebar.radio(
        "Sélectionner une page",
        ["🏠 Vue d'ensemble", "📉 Pauvreté", "🚶 Migration", "🚗 Mobilité", "🗺️ Carte"],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Projet ANStat**")
    st.sidebar.markdown("Standard: UN-MPDMS v2.0")
    st.sidebar.markdown("---")
    st.sidebar.caption("© 2026 - DataLab ANStat")

    # Afficher la page
    if page == "🏠 Vue d'ensemble":
        show_overview(data)
    elif page == "📉 Pauvreté":
        show_poverty_analysis(data)
    elif page == "🚶 Migration":
        show_migration_analysis(data)
    elif page == "🚗 Mobilité":
        show_mobility_analysis(data)
    elif page == "🗺️ Carte":
        show_interactive_map(data)


if __name__ == "__main__":
    main()
