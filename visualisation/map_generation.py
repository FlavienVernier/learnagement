# Ce fichier génère une carte des mobilités via un fichier csv généré à 
# partir d'un programme de scrapping sur le site de poytech dans la rubrique
# https://www.polytech.univ-smb.fr/intranet/international/partir-en-formation/universites-partenaires.html

### Format du csv : University,City,State,ISO-3

import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Chemin du fichier csv
csv_file_path = "visualisation\map_information.csv"

#Charger le fichier CSV en utilisant l'encodage ISO-8859-1 et le point-virgule comme délimiteur
df = pd.read_csv(csv_file_path)

# Initialiser un géocodeur pour obtenir les coordonnées géographiques
geolocator = Nominatim(user_agent="geoapi")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Ajouter des colonnes de latitude et de longitude au DataFrame
def get_coordinates(row):
    location = geocode(f"{row['City']}, {row['State']}, {row['Alpha-3_Code']}")
    return location.latitude if location else None, location.longitude if location else None

df[['Latitude', 'Longitude']] = df.apply(lambda row: pd.Series(get_coordinates(row)), axis=1)


# Filtrer les lignes avec des coordonnées valides
df = df.dropna(subset=['Latitude', 'Longitude'])

# Créer une carte interactive avec Plotly Express
fig = px.scatter_geo(
    df,
    lat='Latitude',
    lon='Longitude',
    hover_name='University',
    scope='world',  # Vous pouvez ajuster à "usa" ou autre si nécessaire
    title="Carte des universités"
)

# Afficher la carte
fig.show()


