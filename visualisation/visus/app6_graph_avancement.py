import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

#Charger les données d'un fichier
file_name = "visualisation/data/Avancement_etu.csv"

def load_data(filename):
    df = pd.read_csv(filename, decimal='.', sep=';')
    return df

#Calculer les avancements
def calcul_avancement(data):
    res = {'Année':0,
           'Année_total':0}
    for _, row in data.iterrows():
        res['Année'] += row['Heure CM fait'] + row['Heure TD fait'] + row['Heure TP fait']
        res['Année_total'] += row['Heure CM total'] + row['Heure TD total'] + row['Heure TP total']
        
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
        res[f"{ue}_total"] += row['Heure CM total'] + row['Heure TD total'] + row['Heure TP total']
            
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

data_brute = load_data(file_name)
data = calcul_avancement(data_brute)
df = transforme_données(data)

# Calculer les pourcentages
df["Completion (%)"] = (df["Realized"] / df["Total"]) * 100

# Catégories par niveau d'agrégation
levels = {
    "Année": ["Année"],
    "Semestre": list(map(str, data_brute['Semestre'].unique())),
    "UE": list(data_brute['Module'].unique()) 
}


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
                color='rgba(44, 168, 235, 0.6)',
                line=dict(color='rgba(44, 168, 235, 1)', width=3)
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
