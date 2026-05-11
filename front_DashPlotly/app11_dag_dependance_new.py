import logging

import dash
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from dash import html, dcc, callback, Input, Output, State
import dash_flows # Remplacez par le vrai nom d'import

import app11_dag_dependance_tools
import app5_module_tools

styles = {
    'width': '100%',
    'height': '600px',
    'border': '1px solid #ccc'
}

app11_new_layout = html.Div([
    dcc.Store(id='app11_edges_precedents', data=[]),
    dcc.Dropdown(
        id='app11_new_filtre_module',
        options=[],
        placeholder="Sélectionnez un module",
    ),
    html.Div(id='sortie_evenements',
             children=["Attente d'une interaction... saved: True"]),
    dash_flows.DashFlows(
                id='app11_new_dag',
                nodes= [],
                edges= [],
                style=styles
            )
])

def register_callbacks(app):
    @app.callback(
        Output('app11_new_filtre_module', 'options'),
        Input('user_id', 'data'),
        Input('role', 'data'),
        State('token', 'data'),
    )
    def update_app11_new_filtre_module_option(user_id, role, token):
        if role == "enseignant":
            df = app5_module_tools.get_moduleByEnseignantId(token, user_id)
        elif role == "etudiant":
            df = app5_module_tools.get_moduleByEtudiantId(token, user_id)
        options = [{'label': row['code_module'], 'value': row['id_module']} for _, row in
                   df[['id_module', 'code_module']].drop_duplicates().iterrows()]
        return options

    @app.callback(
        Output('app11_new_dag', 'nodes'),
        Output('app11_new_dag', 'edges', allow_duplicate=True),
        Output('app11_edges_precedents', 'data', allow_duplicate=True),  # mémoriser l'état
        Output('sortie_evenements', 'children', allow_duplicate=True),
        Input('app11_new_filtre_module', 'value'),
        State('token', 'data'),
        prevent_initial_call=True,
    )
    def update_graph(id_module, token):
        message = " "
        if id_module:
            labels = {}
            df = app11_dag_dependance_tools.get_list_sequence_dependance_by_idModule(token, id_module)
            if not df.empty:
                labels = {
                    str(row["id_module_sequence"]):
                        f"{row['code_module']} - {row['type']}-{row['numero_ordre']}"
                    for _, row in df.iterrows()
                }
            else:
                message = "Aucune sequence, faite votre séquençage avant"
            nodes = []
            edges=[]
            G = nx.DiGraph()
            df = app11_dag_dependance_tools.get_list_dependance_by_idModule(token, id_module)
            if not df.empty:
                edges = [(str(row["id_sequence_prev"]), str(row["id_sequence_next"])) for _, row in df.iterrows() if row["id_sequence_next"] is not None]
                G.add_edges_from(edges)

                G.graph['graph'] = {
                    'rankdir': 'LR'
                }

                pos = graphviz_layout(
                    G,
                    prog="dot"
                )

                edges = [
                    {
                        "id": f"{u}-{v}",
                        "source": u,
                        "target": v
                    }
                    for u, v in G.edges()
                ]

                nodes = [
                    {
                        "id": node,
                        "data": {"label": labels.get(str(node), str(node))},
                        "position": {
                            "x": pos[node][0] * 3,
                            "y": pos[node][1] * 2 + 50
                        }
                    }
                    for node in G.nodes()
                ]
            unlinked_nodes = [n for n in labels.keys() if n not in G.nodes()]
            x=0
            nodes += [
                {
                    "id": node,
                    "data": {"label": labels.get(str(node), str(node))},
                    "position": {
                        "x": i*200,
                        "y": 0
                    }
                }
                for i, node in enumerate(unlinked_nodes)
            ]

            return nodes, edges, edges, message
        return [],[], [], "No module selected"

    # Callback pour réagir aux interactions
    @app.callback(
        Output('app11_new_dag', 'edges'),
        Output('sortie_evenements', 'children'),
        Output('app11_edges_precedents', 'data'),  # mémoriser l'état
        Input('app11_new_dag', 'edges'),
        State('app11_edges_precedents', 'data'),
        State('app11_new_filtre_module', 'value'),
        State('token', 'data'),
        prevent_initial_call=True,
    )
    def gerer_interactions(edges_actuels, edges_precedents, id_module, token):
        if edges_actuels is None:
            raise dash.exceptions.PreventUpdate

        edges_actuels = edges_actuels or []
        edges_precedents = edges_precedents or []

        # --- Détection ajout / suppression ---
        ids_precedents = {e['id']: e for e in edges_precedents}
        ids_actuels = {e['id']: e for e in edges_actuels}

        # Arcs ajoutés
        nouveaux = [e for e in edges_actuels if e['id'] not in ids_precedents]
        # Arcs supprimés
        supprimes = [e for e in edges_precedents if e['id'] not in ids_actuels]

        messages = []
        for e in nouveaux:
            #messages.append(f"Lien créé : {e['source']} → {e['target']}")
            messages.append(
                app11_dag_dependance_tools.add_dependance_to_idModule(
                    token=token,
                    id_module=id_module,
                    id_sequence_prev=e['source'],
                    id_sequence_next=e['target']
                )
            )
        for e in supprimes:
            #messages.append(f"Lien supprimé : {e['source']} → {e['target']}")
            messages.append(
                app11_dag_dependance_tools.delete_dependencie_to_idModule(
                    token=token,
                    id_module=id_module,
                    id_sequence_prev=e['source'],
                    id_sequence_next=e['target']
                )
            )

        # --- Coloriage selon sélection ---
        edges_mis_a_jour = []
        for edge in edges_actuels:
            if edge.get('selected'):
                edge['style'] = {**edge.get('style', {}), 'stroke': '#ff6b6b', 'strokeWidth': 3}
                edge['animated'] = True
            else:
                edge['style'] = {**edge.get('style', {}), 'stroke': '#b1b1b7', 'strokeWidth': 1}
                edge['animated'] = False
            edges_mis_a_jour.append(edge)

        msg_final = " | ".join(messages) if messages else dash.no_update

        return edges_mis_a_jour, msg_final, edges_mis_a_jour