# Ce fichier génère deux graphiques des absences
# par promo de même année et par filière sur toute les années 
# via un fichier csv rempli "à la main" (chaque ligne représente un étudiant)

### Format du csv : filiere,annee,heures_absence

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Chemin du fichier csv
absences_chemin = "visualisation/taux_absenteisme/absences.csv"

# Charger le fichier CSV en utilisant l'encodage ISO-8859-1 et le point-virgule comme délimiteur
data = pd.read_csv(absences_chemin)


# Calculer les heures d'absence totales et la taille des promotions
fusion = (
    pd.DataFrame(data)
    .groupby(["filiere", "annee"])
    .agg(total_heures_absence=("heures_absence", "sum"),
         taille_promo=("heures_absence", "size"))  # 'size' pour compter les lignes
    .reset_index()
)

# Calcul de l'absence moyenne par étudiant (total des heures d'absence divisé par la taille de la promo)
fusion["absence_moyenne"] = fusion["total_heures_absence"] / fusion["taille_promo"]

# Application Dash
app = Dash(__name__)

app.layout = html.Div([
    
    # Dropdown pour sélectionner l'année
    html.Div([
        html.Label("Sélectionnez une année :"),
        dcc.Dropdown(
            id='dropdown-annee',
            options=[{'label': str(annee), 'value': annee} for annee in sorted(fusion['annee'].unique())],
            value=fusion['annee'].unique()[0]  # Valeur par défaut
        )
    ]),
    
    # Bar chart pour les filières d'une année
    dcc.Graph(id='bar-chart-annee'),
    
    html.Hr(),
    
    # Dropdown pour sélectionner la filière
    html.Div([
        html.Label("Sélectionnez une filière :"),
        dcc.Dropdown(
            id='dropdown-filiere',
            options=[{'label': filiere, 'value': filiere} for filiere in sorted(fusion['filiere'].unique())],
            value=fusion['filiere'].unique()[0]  # Valeur par défaut
        )
    ]),
    
    # Bar chart pour les années d'une filière
    dcc.Graph(id='bar-chart-filiere')
])

# Callbacks pour mettre à jour les graphiques en fonction des sélections
@app.callback(
    Output('bar-chart-annee', 'figure'),
    Input('dropdown-annee', 'value')
)
def update_bar_chart_annee(selected_annee):
    # Filtrer les données pour l'année sélectionnée
    filtered_df = fusion[fusion['annee'] == selected_annee]
    # Créer le bar chart avec le l'absence moyenne
    fig = px.bar(
        filtered_df,
        x='filiere',
        y='absence_moyenne',
        title=f"Répartition des absences par filière pour l'année {selected_annee}",
        labels={"filiere": "Filière", "absence_moyenne": "Absence moyenne"}
    )
    return fig

@app.callback(
    Output('bar-chart-filiere', 'figure'),
    Input('dropdown-filiere', 'value')
)
def update_bar_chart_filiere(selected_filiere):
    # Filtrer les données pour la filière sélectionnée
    filtered_df = fusion[fusion['filiere'] == selected_filiere]
    # Créer le bar chart avec l'absence moyenne
    fig = px.bar(
        filtered_df,
        x='annee',
        y='absence_moyenne',
        title=f"Répartition des absences pour la filière {selected_filiere} sur plusieurs années",
        labels={"annee": "Année", "absence_moyenne": "Absence moyenne"}
    )
    
    # Forcer l'axe x à être catégoriel
    fig.update_layout(
        xaxis=dict(
            type='category'  # Assurez-vous que l'axe des années est catégoriel
        )
    )
    
    return fig

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)