from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import app9_rendu_tools

# Définition de la mise en page de l'application
app9_layout = html.Div([
    html.H1("Avancement des rendus par étudiant"),
    dcc.Dropdown(
        id='dropdown_ue',
        # options=[{'label': ue, 'value': ue} for ue in ues],
        options=[{'label': 'Toute UE', 'value': 'Tout'}],
        value='Tout',
        style={'margin-bottom': '10px'}  # Ajouter une marge en bas
    ),
    dcc.Dropdown(
        id='dropdown_module',
        #options=[{'label': etudiant, 'value': etudiant} for etudiant in etudiants],
        options=[{'label': 'Tout module', 'value': 'Tout'}],
        value='Tout',
        #value=etudiants[0], # don't select default if no data
        style={'margin-bottom': '10px'}  # Ajouter une marge en bas
    ),
    dcc.Graph(id='bar_chart')
])

def register_callbacks(app):
    @app.callback(
        Output('dropdown_ue', 'options'),
        Input('user_id', 'data')
    )
    def update_ue_options(user_id):
        ues = app9_rendu_tools.get_renduByEtudianttId(user_id)['learning_unit_name'].drop_duplicates()

        options = [{'label': ue, 'value': ue} for ue in ues]

        return [{'label': 'Toute UE', 'value': 'Tout'}] + options

    @app.callback(
        Output('dropdown_module', 'options'),
        Input('dropdown_ue', 'value'),
        Input('user_id', 'data')
    )
    def update_module_options(selected_ue, user_id):

        if(selected_ue == 'Tout'):
            modules = app9_rendu_tools.get_renduByEtudianttId(user_id)['nom'].drop_duplicates()
        else:
            df=app9_rendu_tools.get_renduByEtudianttId(user_id)
            modules = df[df['learning_unit_name'] == selected_ue]['nom'].drop_duplicates()

        options = [{'label': m, 'value': m} for m in modules]

        return [{'label': 'Tout module', 'value': 'Tout'}] + options

    # Callback pour mettre à jour le bar chart empilé en fonction de l'étudiant et de l'UE sélectionnés
    @app.callback(
        Output('bar_chart', 'figure'),
        Input('dropdown_module', 'value'),
        Input('dropdown_ue', 'value'),
        State('user_id', 'data')
    )
    def update_bar_chart(selected_module, selected_ue, user_id):
        df = app9_rendu_tools.get_renduByEtudianttId(user_id)

        if df.empty:
            return go.Figure()

        #df_etudiant = df[df['nom'] == selected_etudiant]

        if selected_ue != 'Tout':
            df = df[df['learning_unit_name'] == selected_ue]
        elif selected_module != 'Tout':
            df = df[df['nom'] == selected_module]

        # Calculer les rendus terminés et non terminés
        rendus_termines = df['avancement'].sum()
        rendus_non_termines = len(df) - rendus_termines

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
            title=f'Pourcentage de rendus terminés pour {selected_module} ({selected_ue})',
            plot_bgcolor='rgba(0,0,0,0)',  # Enlever le fond du graphique
            paper_bgcolor='rgba(0,0,0,0)'  # Enlever le fond du graphique
        )

        return fig
