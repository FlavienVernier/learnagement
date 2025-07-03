from dotenv import load_dotenv
import os
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import mysql
import mysql.connector

'''
#Charger les données d'un fichier
file_name = "../data/Avancement_etu.csv"

def load_data(filename):
    df = pd.read_csv(filename, decimal='.', sep=';')
    return df'''

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
    database=database,
    auth_plugin='mysql_native_password'
)

# Exécuter la requête pour récupérer les dépendances
cur = conn.cursor()

def get_data_done(id_etudiant) : 
    cur.execute(f"SELECT etu.nom, session.schedule as date_prevue, promo.annee, sequencage.duree_h, module.nom "
                f"FROM CLASS_session as session "
                f"JOIN LNM_groupe as grp ON session.id_groupe = grp.id_groupe "
                f"JOIN LNM_promo as promo ON grp.id_promo = promo.id_promo "
                f"JOIN LNM_etudiant as etu ON grp.id_promo = etu.id_promo "
                f"JOIN MAQUETTE_module_sequence as sequence ON session.id_module_sequence=sequence.id_module_sequence "
                f"JOIN MAQUETTE_module_sequencage as sequencage ON sequence.id_module_sequencage=sequencage.id_module_sequencage "
                f"JOIN MAQUETTE_module as module ON sequencage.id_module=module.id_module "
                f"WHERE session.schedule < CURRENT_DATE and etu.id_etudiant = {id_etudiant};")
    
    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["nom", "date_prevue", "annee", "nb_heure", "matiere"])
    return data

def get_all_data(id_etudiant) : 
    cur.execute(f"SELECT etu.nom, session.schedule as date_prevue, promo.annee, sequencage.duree_h, module.nom "
                f"FROM CLASS_session as session "
                f"JOIN LNM_groupe as grp ON session.id_groupe = grp.id_groupe "
                f"JOIN LNM_promo as promo ON grp.id_promo = promo.id_promo "
                f"JOIN LNM_etudiant as etu ON grp.id_promo = etu.id_promo "
                f"JOIN MAQUETTE_module_sequence as sequence ON session.id_module_sequence=sequence.id_module_sequence "
                f"JOIN MAQUETTE_module_sequencage as sequencage ON sequence.id_module_sequencage=sequencage.id_module_sequencage "
                f"JOIN MAQUETTE_module as module ON sequencage.id_module=module.id_module "
                f"WHERE etu.id_etudiant = {id_etudiant};")

    rows = cur.fetchall()

    # Récupération des données 
    data = pd.DataFrame(rows, columns=["nom", "date_prevue", "annee", "nb_heure", "matiere"])
    return data

num_etudiant = 259

#Calculer les avancements
def calcul_avancement(data_done, data_all):
    res = {'Année':0,
           'Année_total':0}

    res['Année'] = data_done['nb_heure'].sum()
    res['Année_total'] = data_all['nb_heure'].sum()
    
    '''
    for _, row in data_all.iterrows():
        res['Année'] += data_done
        res['Année_total'] += data_all
        
        semestre = str(row['Semestre'])
        if semestre not in res:
            res[semestre] = 0
            res[f"{semestre}_total"] = 0
        
        res[semestre] += row['Heure CM fait'] + row['Heure TD fait'] + row['Heure TP fait']
        res[f"{semestre}_total"] += row['Heure CM total'] + row['Heure TD total'] + row['Heure TP total']
        
        ue = row['Module']
        if ue not in res:
            res[ue] = 0
            res[f"{ue}_total"] = 0
        
        res[ue] += row['Heure CM fait'] + row['Heure TD fait'] + row['Heure TP fait']
        res[f"{ue}_total"] += row['Heure CM total'] + row['Heure TD total'] + row['Heure TP total']'''
            
    return res

def transforme_données(data):
    rows = []
    for key, value in data.items():
        if "_total" not in key:  # Ignorer les clés '_total' dans cette boucle
            total_key = f"{key}_total"
            if total_key in data:
                rows.append({
                    "Category": key,
                    "Realized": value,
                    "Total": data[total_key],
                    "Completion (%)": (value / data[total_key]) * 100 if data[total_key] > 0 else 0
                })
    return pd.DataFrame(rows)

data_done = get_data_done(num_etudiant)
data_all = get_all_data(num_etudiant)
data = calcul_avancement(data_done, data_all)
df = transforme_données(data)

# Calculer les pourcentages
df["Completion (%)"] = (df["Realized"] / df["Total"]) * 100

# Catégories par niveau d'agrégation
'''levels = {
    "Année": ["Année"],
    "Semestre": list(map(str, data_brute['Semestre'].unique())),
    "UE": list(data_brute['Module'].unique())
}'''

levels = {"Année": ["Année"]}


# # Initialiser l'application Dash
# app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.LUX])

app6_layout = html.Div([
    html.H1("Suivi d'Avancement des Cours",
            style={'font-family': 'verdana'}
            ),
    
    # Premier menu déroulant (niveau d'agrégation)
    html.Label("Sélectionnez :",
               style={'margin-left': '5px'}),
    dcc.Dropdown(
        id='level-dropdown',
        options=[{"label": key, "value": key} for key in levels.keys()],
        value="Année",
        style ={
            'width': '50%',
            'margin-left': '5px'
        }
    ),
    
    # Deuxième menu déroulant (catégorie)
    html.Label("Sélectionnez les détails :",
               style={'margin-left': '5px'}),
    dcc.Dropdown(
        id='category-dropdown',
        style ={
            'width': '50%',
            'margin-left': '5px'
        }
    ),
    
    # Graphique
    dcc.Graph(id='progress-chart', style={'marginTop': '30px'})
])

def register_callbacks(app):
    # Callback pour mettre à jour le deuxième menu déroulant
    @app.callback(
        Output('category-dropdown', 'options'),
        Output('category-dropdown', 'value'),
        Input('level-dropdown', 'value')
    )

    def update_category_dropdown(selected_level):
        categories = levels[selected_level]
        options = [{"label": cat, "value": cat} for cat in categories]
        return options, categories[0] 

    # Callback pour mettre à jour le graphique en fonction des sélections
    @app.callback(
        Output('progress-chart', 'figure'),
        Input('level-dropdown', 'value'),
        Input('category-dropdown', 'value')
    )
    def update_graph(selected_level, selected_category):
        # Filtrer les données pour la catégorie sélectionnée
        filtered_df = df[df["Category"] == selected_category]
        
        background_trace = go.Bar(
                x=[100] * len(filtered_df),  # Toutes les barres atteignent 100 %
                y=filtered_df["Category"],
                orientation='h',
                marker=dict(
                    color='rgba(200, 200, 200, 0.4)',
                    line=dict(color='rgba(148, 150, 152, 1)', width=3)
                ),
                hoverinfo='none',
        )

        # Création de la trace des valeurs réelles
        actual_trace = go.Bar(
            x=filtered_df["Completion (%)"],
            y=filtered_df["Category"],
            orientation='h',
            text=filtered_df["Completion (%)"].map(lambda x: f"{x:.0f}%"),
            textposition='inside',
            marker=dict(
                color='rgba(0, 123, 255, 0.6)',
                line=dict(color='rgba(0, 123, 255, 1)', width=3)
            ),
            hoverinfo='none'
        )

        # Création de la figure
        fig = go.Figure(data=[background_trace, actual_trace])

        # Mise en forme de la figure
        fig.update_layout(
            title=f"{selected_category}",
            xaxis=dict(title="Pourcentage d'achèvement", range=[0, 110]),
            yaxis=dict(title='', showticklabels=False),
            barmode='overlay',  # Superposer les barres
            showlegend = False,
            plot_bgcolor='rgba(0,0,0,0)',
        )
        return fig

# # Lancer l'application
# if __name__ == '__main__':
#     app.run_server(debug=True)
