# Ce fichier génère une carte des mobilités via un fichier csv généré à 
# partir d'un programme de scrapping sur le site de poytech dans la rubrique
# https://www.polytech.univ-smb.fr/intranet/international/partir-en-formation/universites-partenaires.html

### Format du csv : University,City,State

import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import plotly.graph_objects as go

# Chemin du fichier csv
csv_file_path = "visualisation\partner_universities.csv"

# Charger le fichier CSV en utilisant l'encodage ISO-8859-1 et le point-virgule comme délimiteur
df = pd.read_csv(csv_file_path)

# Ajouter une colonne combinée pour afficher toutes les universités dans une ville
df_grouped = df.groupby(["City", "Country"])['University'].apply(lambda x: ', '.join(x)).reset_index()
df_grouped.rename(columns={'University': 'Universities'}, inplace=True)

# Ajouter des coordonnées géographiques pour chaque ville et pays
# Utilisation de geopy pour obtenir les coordonnées
geolocator = Nominatim(user_agent="university_map")

# Fonction pour obtenir les coordonnées géographiques
def get_coordinates(row):
    try:
        location = geolocator.geocode(f"{row['City']}, {row['Country']}")
        if location:
            return pd.Series([location.latitude, location.longitude])
    except Exception as e:
        print(f"Erreur pour {row['City']}, {row['Country']}: {e}")
    return pd.Series([None, None])

# Appliquer cette fonction à chaque ligne pour obtenir les coordonnées
df_grouped[['Latitude', 'Longitude']] = df_grouped.apply(get_coordinates, axis=1)

# Supprimer les lignes avec des coordonnées manquantes
df_grouped = df_grouped.dropna(subset=['Latitude', 'Longitude'])

# Initialisation de la figure
fig = go.Figure()

# Ajouter des traces pour chaque pays
countries = df_grouped['Country'].unique()
for country in countries:
    country_data = df_grouped[df_grouped['Country'] == country]
    fig.add_trace(go.Scattermapbox(
        lat=country_data['Latitude'],
        lon=country_data['Longitude'],
        mode='markers',
        marker=dict(size=12, opacity=0.8),
        name=country,  # Nom du pays pour le dropdown
        hoverinfo='text',
         hovertext=country_data.apply(lambda row: f"Université(s): {row['Universities']}<br>Ville: {row['City']}<br>Pays: {row['Country']}", axis=1)
    ))

# Configurer le style de la carte et le menu déroulant
fig.update_layout(
    mapbox=dict(
        style="carto-positron",
        zoom=3,
        center=dict(lat=0, lon=0)
    ),
    updatemenus=[
        dict(
            buttons=[
                dict(
                    args=[{'visible': [country == selected_country for selected_country in countries]}],
                    label=country,
                    method='update'
                ) for country in countries
            ] + [
                dict(
                    args=[{'visible': [True] * len(countries)}],
                    label="Tous",
                    method='update'
                )
            ],
            direction="down",
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top"
        )
    ],
    title="Carte des Universités",
    margin=dict(l=0, r=0, t=30, b=0)
)

# Afficher la carte
fig.show()