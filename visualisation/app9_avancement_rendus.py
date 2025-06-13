from dotenv import load_dotenv
import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import mysql
import plotly.graph_objects as go
import pandas as pd

'''
# Lire le fichier CSV
df = pd.read_csv('../data/avancement_rendus.csv')

# Supprimer les espaces en tête et en queue des noms de colonnes
df.columns = df.columns.str.strip()'''

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

def get_data(id_rendu) : 
    cur.execute(f"SELECT etu.nom, etu.prenom, rm.description, module.nom, ue.learning_unit_name FROM LNM_rendu_module as rm JOIN LNM_rendu_module_as_etudiant as rm_etu ON rm_etu.id_rendu_module=rm.id_rendu_module JOIN LNM_etudiant as etu ON etu.id_etudiant=rm_etu.id_etudiant JOIN MAQUETTE_module_as_learning_unit as mue ON rm.id_module=mue.id_module JOIN MAQUETTE_module as module ON mue.id_module=module.id_module JOIN MAQUETTE_learning_unit as ue ON mue.id_learning_unit=ue.id_learning_unit WHERE rm.id_rendu_module={id_rendu};")
    
    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["nom", "prenom", "description", "matiere", "ue"])
    data["statut"] = 1
    return data

id_rendu = 1
df = get_data(id_rendu)


# Obtenir la liste des noms d'étudiants
etudiants = df['nom'].unique()

# Obtenir la liste des UEs et ajouter l'option 'Tout'
ues = df['ue'].unique()
ues = ['Tout'] + list(ues)

"""# Initialisation de l'application Dash
app = dash.Dash(__name__)"""

# Définition de la mise en page de l'application
app9_layout = html.Div([
    html.H1("Avancement des rendus par étudiant"),
    dcc.Dropdown(
        id='dropdown-etudiant',
        options=[{'label': etudiant, 'value': etudiant} for etudiant in etudiants],
        value=etudiants[0],
        style={'margin-bottom': '10px'}  # Ajouter une marge en bas
    ),
    dcc.Dropdown(
        id='dropdown-ue',
        options=[{'label': ue, 'value': ue} for ue in ues],
        value='Tout',
        style={'margin-bottom': '10px'}  # Ajouter une marge en bas
    ),
    dcc.Graph(id='bar-chart')
])

def register_callbacks(app):
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

        # Calculer les pourcentages
        total_rendus = rendus_termines + rendus_non_termines
        pourcentage_termines = (rendus_termines / total_rendus) * 100
        pourcentage_non_termines = (rendus_non_termines / total_rendus) * 100

        df_pourcentage = pd.DataFrame({
            'Statut': ['Terminés', 'Non terminés'],
            'Pourcentage': [pourcentage_termines, pourcentage_non_termines]
        })

        # Créer le bar chart empilé horizontal
        fig = go.Figure(data=[
            go.Bar(
                name='Terminés', 
                y=df_pourcentage['Statut'], 
                x=df_pourcentage[df_pourcentage['Statut'] == 'Terminés']['Pourcentage'], 
                text=df_pourcentage[df_pourcentage['Statut'] == 'Terminés']['Pourcentage'].round().astype(int).astype(str) + '%',
                textposition='inside',
                orientation='h', 
                marker=dict(
                color='rgba(0, 123, 255, 0.6)',
                line=dict(color='rgba(0, 123, 255, 1)', width=3)
            ),
                hoverinfo='none'),
            go.Bar(
                name='Non terminés', 
                y=df_pourcentage['Statut'], 
                x=df_pourcentage[df_pourcentage['Statut'] == 'Non terminés']['Pourcentage'], 
                orientation='h', 
                marker=dict(
                color='rgba(255, 132, 0, 0.6)',
                line=dict(color='rgba(255, 132, 0, 1)', width=3)
            ),
                hoverinfo='none')
        ])

        # Modifier la disposition pour les barres empilées et enlever le fond du graphique
        fig.update_layout(
            barmode='stack',
            title=f'Pourcentage de rendus terminés pour {selected_etudiant} ({selected_ue})',
            plot_bgcolor='rgba(0,0,0,0)',  # Enlever le fond du graphique
            paper_bgcolor='rgba(0,0,0,0)'  # Enlever le fond du graphique
        )

        return fig

"""# Exécution de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
"""
