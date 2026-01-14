"""
Composant de visualisation temporelle de la mobilité
À ajouter dans src/dashboard/app.py ou comme page séparée

Dépendances supplémentaires:
    pip install pydeck streamlit-folium
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def generate_temporal_mobility_data(
    n_days: int = 365, n_users: int = 1000
) -> pd.DataFrame:
    """
    Génère des données de mobilité temporelles simulées pour toute l'année.
    En production, ces données viendraient des CDR réels.
    """
    np.random.seed(42)

    # Localités principales avec coordonnées
    localities = {
        "Abidjan": {"lat": 5.36, "lon": -4.01, "weight": 0.35},
        "Bouaké": {"lat": 7.69, "lon": -5.03, "weight": 0.12},
        "Yamoussoukro": {"lat": 6.82, "lon": -5.28, "weight": 0.08},
        "Korhogo": {"lat": 9.46, "lon": -5.63, "weight": 0.07},
        "San-Pédro": {"lat": 4.75, "lon": -6.64, "weight": 0.06},
        "Daloa": {"lat": 6.88, "lon": -6.45, "weight": 0.05},
        "Man": {"lat": 7.41, "lon": -7.55, "weight": 0.05},
        "Gagnoa": {"lat": 6.13, "lon": -5.95, "weight": 0.04},
        "Abengourou": {"lat": 6.73, "lon": -3.50, "weight": 0.04},
        "Divo": {"lat": 5.84, "lon": -5.36, "weight": 0.04},
        "Bondoukou": {"lat": 8.04, "lon": -2.80, "weight": 0.03},
        "Odienné": {"lat": 9.51, "lon": -7.57, "weight": 0.03},
        "Séguéla": {"lat": 7.96, "lon": -6.67, "weight": 0.02},
        "Ferkessédougou": {"lat": 9.59, "lon": -5.19, "weight": 0.02},
    }

    records = []
    start_date = datetime(2025, 1, 1)

    for day in range(n_days):
        current_date = start_date + timedelta(days=day)
        month = current_date.month
        day_of_week = current_date.weekday()

        # Facteurs saisonniers
        # Plus de mobilité vers Abidjan en septembre-octobre (rentrée)
        # Plus de mobilité vers les régions en décembre (fêtes)
        seasonal_factor = 1.0
        if month in [9, 10]:  # Rentrée
            seasonal_factor = 1.3
        elif month == 12:  # Fêtes
            seasonal_factor = 1.5
        elif month in [7, 8]:  # Vacances
            seasonal_factor = 1.2
        elif month in [4, 5, 6]:  # Saison des pluies
            seasonal_factor = 0.8

        # Moins de mobilité le weekend
        if day_of_week >= 5:
            seasonal_factor *= 0.7

        # Nombre de mouvements ce jour
        n_movements = int(np.random.poisson(50 * seasonal_factor))

        for _ in range(n_movements):
            # Choisir origine et destination
            locs = list(localities.keys())
            weights = [localities[l]["weight"] for l in locs]

            origin = np.random.choice(locs, p=weights)
            # Destination biaisée vers Abidjan
            dest_weights = weights.copy()
            dest_weights[0] *= 2  # Abidjan plus attractif
            dest_weights = [w / sum(dest_weights) for w in dest_weights]
            destination = np.random.choice(locs, p=dest_weights)

            if origin != destination:
                records.append(
                    {
                        "date": current_date,
                        "month": month,
                        "week": current_date.isocalendar()[1],
                        "day_of_week": day_of_week,
                        "origin": origin,
                        "origin_lat": localities[origin]["lat"],
                        "origin_lon": localities[origin]["lon"],
                        "destination": destination,
                        "dest_lat": localities[destination]["lat"],
                        "dest_lon": localities[destination]["lon"],
                        "flow_count": np.random.randint(1, 20),
                        "migration_type": np.random.choice(
                            ["Travail", "Études", "Famille", "Commerce", "Autre"],
                            p=[0.35, 0.20, 0.25, 0.12, 0.08],
                        ),
                    }
                )

    return pd.DataFrame(records)


def show_temporal_mobility_page():
    """
    Page de visualisation temporelle de la mobilité.
    Ajouter cette fonction dans le menu principal du dashboard.
    """
    st.markdown("## 🎬 Mobilité dans le Temps")
    st.markdown(
        "Visualisez l'évolution des flux de mobilité tout au long de l'année 2025."
    )

    # Charger ou générer les données
    @st.cache_data
    def load_temporal_data():
        return generate_temporal_mobility_data()

    df = load_temporal_data()

    # ===== CONTRÔLES DANS LA PAGE PRINCIPALE =====
    st.markdown("### ⏱️ Contrôles temporels")

    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 2, 1])

    with ctrl_col1:
        # Sélection de la granularité
        granularity = st.selectbox(
            "Granularité",
            ["Jour", "Semaine", "Mois"],
            index=2,
            key="temporal_granularity",
        )

    # Réinitialiser le slider si la granularité change
    if "prev_granularity" not in st.session_state:
        st.session_state.prev_granularity = granularity
    if st.session_state.prev_granularity != granularity:
        st.session_state.prev_granularity = granularity
        if "temporal_time_slider" in st.session_state:
            del st.session_state["temporal_time_slider"]

    # Sélection de la période
    if granularity == "Mois":
        time_col = "month"
        time_labels = {
            1: "Janvier",
            2: "Février",
            3: "Mars",
            4: "Avril",
            5: "Mai",
            6: "Juin",
            7: "Juillet",
            8: "Août",
            9: "Septembre",
            10: "Octobre",
            11: "Novembre",
            12: "Décembre",
        }
        min_val, max_val = 1, 12
    elif granularity == "Semaine":
        time_col = "week"
        time_labels = {i: f"Semaine {i}" for i in range(1, 53)}
        min_val, max_val = 1, 52
    else:
        time_col = "date"
        time_labels = None
        min_val, max_val = 0, 364

    with ctrl_col3:
        # Mode animation
        animation_mode = st.checkbox(
            "🎬 Mode animation", value=False, key="temporal_animation_mode"
        )

    # Initialiser selected_time avec une valeur par défaut
    selected_time = 1

    with ctrl_col2:
        if not animation_mode:
            if granularity in ["Mois", "Semaine"]:
                selected_time = st.slider(
                    f"Sélectionner le {granularity.lower()}",
                    min_value=min_val,
                    max_value=max_val,
                    value=min_val,
                    key="temporal_time_slider",
                )
                if time_labels:
                    st.info(
                        f"📅 Période sélectionnée : **{time_labels[selected_time]}**"
                    )
            else:
                selected_date = st.date_input(
                    "Sélectionner une date",
                    value=datetime(2025, 1, 1),
                    min_value=datetime(2025, 1, 1),
                    max_value=datetime(2025, 12, 31),
                    key="temporal_date_input",
                )
                selected_time = selected_date
        else:
            st.info(
                "🎬 **Mode animation activé** - Utilisez les contrôles de lecture sur les graphiques"
            )

    st.markdown("---")

    # Filtrer les données
    filtered_df = df.copy()  # Valeur par défaut
    if animation_mode:
        # Mode animation - utiliser Plotly animation
        filtered_df = df  # Toutes les données pour l'animation
    else:
        if granularity == "Jour":
            filtered_df = df[df["date"].dt.date == selected_time]
        else:
            filtered_df = df[df[time_col] == selected_time]

    # ===== MÉTRIQUES =====
    col1, col2, col3, col4 = st.columns(4)

    if not animation_mode:
        with col1:
            st.metric("🚶 Mouvements", f"{len(filtered_df):,}")
        with col2:
            st.metric("📍 Origines", filtered_df["origin"].nunique())
        with col3:
            st.metric("🎯 Destinations", filtered_df["destination"].nunique())
        with col4:
            total_flow = filtered_df["flow_count"].sum()
            st.metric("👥 Flux total", f"{total_flow:,}")

    # ===== VISUALISATIONS =====

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🗺️ Carte des flux",
            "📊 Évolution annuelle",
            "🔥 Heatmap temporelle",
            "🏆 Top destinations",
        ]
    )

    with tab1:
        st.markdown("### Carte des flux de mobilité")

        if animation_mode:
            # Animation par mois avec Plotly
            monthly_flows = (
                df.groupby(
                    [
                        "month",
                        "origin",
                        "destination",
                        "origin_lat",
                        "origin_lon",
                        "dest_lat",
                        "dest_lon",
                    ]
                )
                .agg({"flow_count": "sum"})
                .reset_index()
            )

            monthly_flows["month_name"] = monthly_flows["month"].map(
                {
                    1: "Janvier",
                    2: "Février",
                    3: "Mars",
                    4: "Avril",
                    5: "Mai",
                    6: "Juin",
                    7: "Juillet",
                    8: "Août",
                    9: "Septembre",
                    10: "Octobre",
                    11: "Novembre",
                    12: "Décembre",
                }
            )

            # Créer les points pour la carte animée
            fig = px.scatter_mapbox(
                monthly_flows,
                lat="dest_lat",
                lon="dest_lon",
                size="flow_count",
                color="destination",
                hover_name="destination",
                hover_data={
                    "origin": True,
                    "flow_count": True,
                    "dest_lat": False,
                    "dest_lon": False,
                },
                animation_frame="month_name",
                mapbox_style="carto-positron",
                center={"lat": 7.54, "lon": -5.55},
                zoom=5.5,
                size_max=40,
                title="Animation des flux de mobilité par mois",
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True, key="temporal_map_animated")

        else:
            # Carte statique pour la période sélectionnée
            if not filtered_df.empty:
                # Agréger les flux par O-D
                flow_agg = (
                    filtered_df.groupby(
                        [
                            "origin",
                            "destination",
                            "origin_lat",
                            "origin_lon",
                            "dest_lat",
                            "dest_lon",
                        ]
                    )["flow_count"]
                    .sum()
                    .reset_index()
                )

                # Créer la figure avec lignes de flux
                fig = go.Figure()

                # Ajouter les lignes de flux
                for _, row in flow_agg.iterrows():
                    fig.add_trace(
                        go.Scattermapbox(
                            mode="lines",
                            lon=[row["origin_lon"], row["dest_lon"]],
                            lat=[row["origin_lat"], row["dest_lat"]],
                            line=dict(
                                width=max(1, row["flow_count"] / 10), color="#FF6B00"
                            ),
                            opacity=0.6,
                            hoverinfo="text",
                            text=f"{row['origin']} → {row['destination']}: {row['flow_count']} flux",
                            showlegend=False,
                        )
                    )

                # Ajouter les points de destination
                dest_agg = (
                    filtered_df.groupby(["destination", "dest_lat", "dest_lon"])[
                        "flow_count"
                    ]
                    .sum()
                    .reset_index()
                )
                fig.add_trace(
                    go.Scattermapbox(
                        mode="markers",
                        lon=dest_agg["dest_lon"],
                        lat=dest_agg["dest_lat"],
                        marker=dict(
                            size=dest_agg["flow_count"]
                            / dest_agg["flow_count"].max()
                            * 30
                            + 10,
                            color="#FF6B00",
                            opacity=0.8,
                        ),
                        text=dest_agg["destination"],
                        hoverinfo="text",
                        showlegend=False,
                    )
                )

                fig.update_layout(
                    mapbox=dict(
                        style="carto-positron",
                        center={"lat": 7.54, "lon": -5.55},
                        zoom=5.5,
                    ),
                    height=600,
                    margin={"r": 0, "t": 30, "l": 0, "b": 0},
                    title=f"Flux de mobilité - {time_labels[selected_time] if time_labels else selected_time}",
                )
                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key=f"temporal_map_static_{selected_time}",
                )
            else:
                st.warning("Aucune donnée pour cette période")

    with tab2:
        st.markdown("### 📈 Évolution des flux sur l'année")

        # Agrégation mensuelle
        monthly_total = (
            df.groupby("month")
            .agg({"flow_count": "sum", "origin": "count"})
            .reset_index()
        )
        monthly_total.columns = ["Mois", "Flux total", "Nb mouvements"]
        monthly_total["Mois_nom"] = monthly_total["Mois"].map(
            {
                1: "Jan",
                2: "Fév",
                3: "Mar",
                4: "Avr",
                5: "Mai",
                6: "Juin",
                7: "Juil",
                8: "Août",
                9: "Sep",
                10: "Oct",
                11: "Nov",
                12: "Déc",
            }
        )

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=monthly_total["Mois_nom"],
                y=monthly_total["Flux total"],
                name="Flux total",
                marker_color="#FF6B00",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=monthly_total["Mois_nom"],
                y=monthly_total["Nb mouvements"] * 10,
                name="Nb mouvements (×10)",
                mode="lines+markers",
                line=dict(color="#2E86AB", width=3),
            )
        )

        # Marquer les événements clés
        fig.add_annotation(
            x="Sep",
            y=monthly_total[monthly_total["Mois"] == 9]["Flux total"].values[0],
            text="📚 Rentrée",
            showarrow=True,
            arrowhead=2,
        )
        fig.add_annotation(
            x="Déc",
            y=monthly_total[monthly_total["Mois"] == 12]["Flux total"].values[0],
            text="🎄 Fêtes",
            showarrow=True,
            arrowhead=2,
        )

        fig.update_layout(
            title="Évolution mensuelle des flux de mobilité",
            xaxis_title="Mois",
            yaxis_title="Volume",
            legend=dict(x=0.7, y=1),
            height=400,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Graphique par type de migration
        st.markdown("#### Par type de migration")
        type_monthly = (
            df.groupby(["month", "migration_type"])["flow_count"].sum().reset_index()
        )
        type_monthly["Mois_nom"] = type_monthly["month"].map(
            {
                1: "Jan",
                2: "Fév",
                3: "Mar",
                4: "Avr",
                5: "Mai",
                6: "Juin",
                7: "Juil",
                8: "Août",
                9: "Sep",
                10: "Oct",
                11: "Nov",
                12: "Déc",
            }
        )

        fig2 = px.area(
            type_monthly,
            x="Mois_nom",
            y="flow_count",
            color="migration_type",
            title="Flux par type de migration",
            labels={"flow_count": "Flux", "migration_type": "Type"},
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.markdown("### 🔥 Heatmap : Intensité par mois et destination")

        # Créer la matrice mois x destination
        heatmap_data = (
            df.groupby(["month", "destination"])["flow_count"].sum().reset_index()
        )
        pivot = heatmap_data.pivot(
            index="destination", columns="month", values="flow_count"
        ).fillna(0)

        # Renommer les colonnes
        pivot.columns = [
            "Jan",
            "Fév",
            "Mar",
            "Avr",
            "Mai",
            "Juin",
            "Juil",
            "Août",
            "Sep",
            "Oct",
            "Nov",
            "Déc",
        ]

        fig = px.imshow(
            pivot,
            labels=dict(x="Mois", y="Destination", color="Flux"),
            color_continuous_scale="YlOrRd",
            aspect="auto",
            title="Intensité des flux par destination et mois",
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Heatmap jour de la semaine x heure (simulé)
        st.markdown("#### Pattern hebdomadaire")
        week_pattern = df.groupby("day_of_week")["flow_count"].sum().reset_index()
        week_pattern["Jour"] = week_pattern["day_of_week"].map(
            {
                0: "Lundi",
                1: "Mardi",
                2: "Mercredi",
                3: "Jeudi",
                4: "Vendredi",
                5: "Samedi",
                6: "Dimanche",
            }
        )

        fig3 = px.bar(
            week_pattern,
            x="Jour",
            y="flow_count",
            color="flow_count",
            color_continuous_scale="YlOrRd",
            title="Flux par jour de la semaine",
        )
        fig3.update_layout(height=350)
        st.plotly_chart(fig3, use_container_width=True)

    with tab4:
        st.markdown("### 🏆 Top destinations animé (Racing Bar Chart)")

        # Données pour le racing bar chart
        monthly_dest = (
            df.groupby(["month", "destination"])["flow_count"].sum().reset_index()
        )
        monthly_dest["month_name"] = monthly_dest["month"].map(
            {
                1: "01-Janvier",
                2: "02-Février",
                3: "03-Mars",
                4: "04-Avril",
                5: "05-Mai",
                6: "06-Juin",
                7: "07-Juillet",
                8: "08-Août",
                9: "09-Septembre",
                10: "10-Octobre",
                11: "11-Novembre",
                12: "12-Décembre",
            }
        )

        # Calculer le cumul
        monthly_dest_sorted = monthly_dest.sort_values(["destination", "month"])
        monthly_dest_sorted["cumul"] = monthly_dest_sorted.groupby("destination")[
            "flow_count"
        ].cumsum()

        fig = px.bar(
            monthly_dest_sorted,
            x="cumul",
            y="destination",
            color="destination",
            animation_frame="month_name",
            orientation="h",
            title="Course des destinations - Flux cumulés",
            labels={"cumul": "Flux cumulé", "destination": "Destination"},
        )
        fig.update_layout(
            height=600, showlegend=False, yaxis={"categoryorder": "total ascending"}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Tableau récapitulatif
        st.markdown("#### 📊 Récapitulatif annuel")
        annual_summary = (
            df.groupby("destination")
            .agg({"flow_count": "sum", "origin": "count"})
            .reset_index()
        )
        annual_summary.columns = ["Destination", "Flux total", "Nb mouvements"]
        annual_summary = annual_summary.sort_values("Flux total", ascending=False)
        annual_summary["Part (%)"] = (
            annual_summary["Flux total"] / annual_summary["Flux total"].sum() * 100
        ).round(1)

        st.dataframe(annual_summary, use_container_width=True, hide_index=True)

    # ===== EXPORT =====
    st.markdown("---")
    st.markdown("### 💾 Export des données")

    col1, col2 = st.columns(2)
    with col1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Télécharger toutes les données (CSV)",
            csv,
            "mobilite_temporelle_2025.csv",
            "text/csv",
        )
    with col2:
        if not animation_mode:
            csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                f"📥 Télécharger période sélectionnée (CSV)",
                csv_filtered,
                f"mobilite_{selected_time}.csv",
                "text/csv",
            )


# Pour intégrer dans le dashboard principal, ajouter dans main():
# if page == "🎬 Mobilité Temporelle":
#     show_temporal_mobility_page()

if __name__ == "__main__":
    st.set_page_config(page_title="Mobilité Temporelle", layout="wide")
    show_temporal_mobility_page()
