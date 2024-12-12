# Ce fichier génère une carte des mobilités via un fichier csv généré à 
# partir d'un programme de scrapping sur le site de poytech dans la rubrique
# https://www.polytech.univ-smb.fr/intranet/international/partir-en-formation/universites-partenaires.html

### Format du csv : University,City,State

import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Chemin du fichier csv
csv_file_path = "visualisation\map_information.csv"

#Charger le fichier CSV en utilisant l'encodage ISO-8859-1 et le point-virgule comme délimiteur
df = pd.read_csv(csv_file_path)

# Ajouter une colonne combinée pour afficher toutes les universités dans une ville
df_grouped = df.groupby(["City", "Country"])['University'].apply(lambda x: ', '.join(x)).reset_index()
df_grouped.rename(columns={'University': 'Universities'}, inplace=True)

# Ajouter des coordonnées géographiques pour chaque ville et pays
# Utilisation de geopy pour obtenir les coordonnées
from geopy.geocoders import Nominatim

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

# Créer une carte avec Plotly Express
fig = px.scatter_mapbox(
    df_grouped,
    lat="Latitude",
    lon="Longitude",
    hover_name="Universities",
    hover_data={"City": True, "Country": True, "Latitude": False, "Longitude": False},
    mapbox_style="carto-positron",
    zoom=3,
    color="Country",
    title="Carte des Universités"
)
fig.update_traces(marker=dict(size=12, opacity=0.8))
# Afficher la carte
fig.show()
