from dotenv import load_dotenv
import os
import mysql
import mysql.connector
import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

load_dotenv()

user = os.getenv("MYSQL_USER_LOGIN")
password = os.getenv("MYSQL_USER_PASSWORD")
host = os.getenv("MYSQL_SERVER")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DB")

# Se connecter à la base de données MySQL
conn = mysql.connector.connect(
    user=user,
    password=password,
    host=host,
    port=port,
    database=database
)

# Exécuter la requête pour récupérer les dépendances
cur = conn.cursor()

#cur.execute("SELECT * FROM VIEW_graphe_dependances")
cur.execute("SELECT nom, ville, pays FROM LNM_universite")

rows = cur.fetchall()

df = pd.DataFrame(rows, columns=["University", "City", "Country"])

# Ajouter une colonne combinée pour afficher toutes les universités dans une ville
df_grouped = df.groupby(["City", "Country"])['University'].apply(lambda x: ', '.join(x)).reset_index()
df_grouped.rename(columns={'University': 'Universities'}, inplace=True)

# Ajouter des coordonnées géographiques pour chaque ville et pays
geolocator = Nominatim(user_agent="university_map")

# Fonction pour obtenir les coordonnées géographiques
def get_coordinates(row):
    try:
        location = geolocator.geocode(f"{row['City']}, {row['Country']}", timeout=10)
        if location:
            return pd.Series([location.latitude, location.longitude])
    except Exception as e:
        print(f"Erreur pour {row['City']}, {row['Country']}: {e}")
    return pd.Series([None, None])

# Appliquer cette fonction à chaque ligne pour obtenir les coordonnées
df_grouped[['Latitude', 'Longitude']] = df_grouped.apply(get_coordinates, axis=1)

# Supprimer les lignes avec des coordonnées manquantes
df_grouped = df_grouped.dropna(subset=['Latitude', 'Longitude'])

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app1_layout = html.Div(
    children=[
        html.Div([
            html.H1("Carte des Universités Partenaires", style={"textAlign": "center"}),
            dcc.Dropdown(
                id="country-dropdown",
                options=[{"label": "Tous", "value": "Tous"}] + [{"label": country, "value": country} for country in df_grouped['Country'].unique()],
                value="Tous",
                clearable=False,
                style={"width": "60%", "margin": "auto"}
            ),
            dcc.Graph(
                id="university-map",
                style={"height": "600px", "marginTop": "20px"}
            )
        ], style={
            "backgroundColor": "white",
            "padding": "30px",
            "margin": "40px auto",
            "width": "90%",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
            "borderRadius": "15px"
        })
    ]
)


def register_callbacks(app):
    # Callback pour mettre à jour la carte en fonction du pays sélectionné
    @app.callback(
        Output("university-map", "figure"),
        [Input("country-dropdown", "value")]
    )
    def update_map(selected_country):
        if selected_country == "Tous":
            filtered_data = df_grouped
        else:
            filtered_data = df_grouped[df_grouped["Country"] == selected_country]
        
        # Calculer le centre de la carte
        center_lat = filtered_data['Latitude'].mean()
        center_lon = filtered_data['Longitude'].mean()
        
        # Initialisation de la figure
        fig = go.Figure()

        # Ajouter des traces pour chaque pays (ou toutes les données si "Tous" est sélectionné)
        countries = filtered_data['Country'].unique()
        for country in countries:
            country_data = filtered_data[filtered_data['Country'] == country]
            fig.add_trace(go.Scattermapbox(
                lat=country_data['Latitude'],
                lon=country_data['Longitude'],
                mode='markers',
                marker=dict(size=12, opacity=0.8),
                hoverinfo='text',
                hovertext=country_data.apply(lambda row: f"Université(s): {row['Universities']}<br>Ville: {row['City']}<br>Pays: {row['Country']}", axis=1),
                showlegend=False  # Désactive l'affichage des traces dans la légende
            ))

        # Configuration de la carte
        fig.update_layout(
            mapbox=dict(
                style="carto-positron",
                zoom=3,
                center=dict(lat=center_lat, lon=center_lon)
            ),
            title="Carte des Universités",
            margin=dict(l=0, r=0, t=30, b=0)
        )

        return fig

# if __name__ == "__main__":
#     app.run_server(debug=True)
