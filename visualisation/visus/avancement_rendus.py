import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Lire le fichier CSV
df = pd.read_csv('visualisation/data/avancement_rendus.csv')

# Supprimer les espaces en tête et en queue des noms de colonnes
df.columns = df.columns.str.strip()

# Obtenir la liste des noms d'étudiants
etudiants = df['nom'].unique()

# Obtenir la liste des UEs et ajouter l'option 'Tout'
ues = df['ue'].unique()
ues = ['Tout'] + list(ues)

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Définition de la mise en page de l'application
app.layout = html.Div([
    html.H1("Avancement des rendus par étudiant"),
    dcc.Dropdown(
        id='dropdown-etudiant',
        options=[{'label': etudiant, 'value': etudiant} for etudiant in etudiants],
        value=etudiants[0],
        style={'margin-bottom': '20px'}  # Ajouter une marge en bas
    ),
    dcc.Dropdown(
        id='dropdown-ue',
        options=[{'label': ue, 'value': ue} for ue in ues],
        value='Tout',
        style={'margin-bottom': '20px'}  # Ajouter une marge en bas
    ),
    dcc.Graph(id='bar-chart')
])

# Callback pour mettre à jour le bar chart empilé en fonction de l'étudiant et de l'UE sélectionnés
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('dropdown-etudiant', 'value'),
     Input('dropdown-ue', 'value')]
)
def update_bar_chart(selected_etudiant, selected_ue):
    df_etudiant = df[df['nom'] == selected_etudiant]

    if selected_ue != 'Tout':
        df_etudiant = df_etudiant[df_etudiant['ue'] == selected_ue]

    # Calculer les rendus terminés et non terminés
    rendus_termines = df_etudiant['statut'].sum()
    rendus_non_termines = len(df_etudiant) - rendus_termines

    df_pourcentage = pd.DataFrame({
        'Statut': ['Terminés', 'Non terminés'],
        'Pourcentage': [rendus_termines, rendus_non_termines]
    })

    # Créer le bar chart empilé horizontal
    fig = go.Figure(data=[
        go.Bar(name='Terminés', y=df_pourcentage['Statut'], x=df_pourcentage[df_pourcentage['Statut'] == 'Terminés']['Pourcentage'], orientation='h', marker_color='green'),
        go.Bar(name='Non terminés', y=df_pourcentage['Statut'], x=df_pourcentage[df_pourcentage['Statut'] == 'Non terminés']['Pourcentage'], orientation='h', marker_color='red')
    ])

    # Modifier la disposition pour les barres empilées
    fig.update_layout(barmode='stack', title=f'Pourcentage de rendus terminés pour {selected_etudiant} ({selected_ue})')

    return fig

# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
