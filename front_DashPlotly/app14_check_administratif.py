import logging
import networkx as nx
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import app14_check_tools
import pandas as pd

# Définition de la mise en page de l'application
app14_administratif_layout = html.Div(children=[
    dbc.Button(
        'Séquençage VS Maquette',
            id="collapse-button1",
            className="mb-3",
            color="primary",
            n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
                 style={'display': 'inline-block', 'verticalAlign': 'top',},
                 children=[
                    dcc.Input(id='fake', value='0', type='hidden'),
                     html.Div(id='table_sequencage_vs_maquette')]
             ),
        id="collapse1",
        is_open=False,
    ),
    html.Br(),
    # dbc.Button(
    #     'Session VS Maquette',
    #         id="collapse_button_session_vs_maquette",
    #         className="mb-3",
    #         color="primary",
    #         n_clicks=0,
    # ),
    # dbc.Collapse(
    #     html.Div(
    #              style={'display': 'inline-block', 'verticalAlign': 'top',},
    #              children=[
    #                 dcc.Input(id='fake', value='0', type='hidden'),
    #                  html.Div(id='table_session_vs_maquette')]
    #          ),
    #     id="collapse_session_vs_maquette",
    #     is_open=False,
    # ),
    # html.Br(),
    dbc.Button(
        'Modules sans UE',
        id="collapse-button2",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='table_modules_sans_ue')]
        ),
        id="collapse2",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Modules sans AC',
        id="collapse-button3",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='table_modules_sans_ac')]
        ),
        id="collapse3",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Enseignant sans cours',
        id="collapse-button4",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='div_enseignant_sans_cours')]
        ),
        id="collapse4",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Session sans enseignant',
        id="collapse-button5",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='div_session_sans_enseignant')]
        ),
        id="collapse5",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Poids ECTS',
        id="collapse-button6",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='div_modules_ects')]
        ),
        id="collapse6",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Corruption d\'intégrité référentielle dans la table session',
        id="collapse-button7",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='div_session_corruption')]
        ),
        id="collapse7",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'Graph des permissions',
        id="collapse-button8",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='div_auth')]
        ),
        id="collapse8",
        is_open=False,
    ),
    html.Br(),
    dbc.Button(
        'DAG des permissions',
        id="collapse-button9",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        html.Div(
            style={'display': 'inline-block', 'verticalAlign': 'top',},
            children=[
                dcc.Input(id='fake', value='0', type='hidden'),
                html.Div(id='div_auth_tree_sqlglot')]
        ),
        id="collapse9",
        is_open=False,
    ),
])


######################################
# Callbacks
######################################

def register_callbacks(app):

    @app.callback(
        Output("collapse1", "is_open"),
        [Input("collapse-button1", "n_clicks")],
        [State("collapse1", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # @app.callback(
    #     Output("collapse_session_vs_maquette", "is_open"),
    #     [Input("collapse_button_session_vs_maquette", "n_clicks")],
    #     [State("collapse_session_vs_maquette", "is_open")],
    # )
    # def toggle_collapse(n, is_open):
    #     if n:
    #         return not is_open
    #     return is_open

    @app.callback(
        Output("collapse2", "is_open"),
        [Input("collapse-button2", "n_clicks")],
        [State("collapse2", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse3", "is_open"),
        [Input("collapse-button3", "n_clicks")],
        [State("collapse3", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse4", "is_open"),
        [Input("collapse-button4", "n_clicks")],
        [State("collapse4", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse5", "is_open"),
        [Input("collapse-button5", "n_clicks")],
        [State("collapse5", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse6", "is_open"),
        [Input("collapse-button6", "n_clicks")],
        [State("collapse6", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse7", "is_open"),
        [Input("collapse-button7", "n_clicks")],
        [State("collapse7", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse8", "is_open"),
        [Input("collapse-button8", "n_clicks")],
        [State("collapse8", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output("collapse9", "is_open"),
        [Input("collapse-button9", "n_clicks")],
        [State("collapse9", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    @app.callback(
        Output(component_id='table_sequencage_vs_maquette', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.check_sequencage_vs_maquette(token)
        table_sequencage_vs_maquette = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_sequencage_vs_maquette]

    @app.callback(
        Output(component_id='table_session_vs_maquette', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.check_session_vs_maquette(token)
        if df.empty:
            df = pd.DataFrame(columns=['truc', 'bidule'])
        table_session_vs_maquette = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_session_vs_maquette]


    @app.callback(
        Output(component_id='table_modules_sans_ue', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.check_module_without_learning_unit(token)
        table_modules_sans_ue = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_modules_sans_ue]


    @app.callback(
        Output(component_id='table_modules_sans_ac', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.check_module_without_apprentissage_critique(token)
        table_modules_sans_ac = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_modules_sans_ac]


    @app.callback(
        Output(component_id='div_enseignant_sans_cours', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.check_enseignant_sans_cours(token)
        table_enseignant_sans_cours = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_enseignant_sans_cours]


    @app.callback(
        Output(component_id='div_session_sans_enseignant', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.check_session_sans_enseignant(token)
        table_session_sans_enseignant = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_session_sans_enseignant]


    @app.callback(
        Output(component_id='div_modules_ects', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.check_module_ects(token)
        table_modules_ects = dbc.Table.from_dataframe(
            df,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_modules_ects]

    @app.callback(
        Output(component_id='div_session_corruption', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.check_session_corruption(token)
        if not df.empty:
            table_session_corruption = dbc.Table.from_dataframe(
                df,
                # Key styling options:
                striped=True,
                bordered=True,
                hover=True,
            )
            return [table_session_corruption]
        return [html.Label("No data available")]

    @app.callback(
        Output(component_id='div_auth', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_table(user_id_fake, token):
        df = app14_check_tools.get_access_auth(token)
        logging.info(df)
        if not df.empty:
            table_access_auth = dbc.Table.from_dataframe(
                df,
                # Key styling options:
                striped=True,
                bordered=True,
                hover=True,
            )
            logging.info(table_access_auth)
            return [table_access_auth]
        return [html.Label("No data available")]

    def build_graph_from_tree(node: dict, G: nx.DiGraph = None) -> nx.DiGraph:
        """Construit un DiGraph NetworkX récursivement depuis l'arbre JSON."""
        if G is None:
            G = nx.DiGraph()

        node_id = node["id"]
        node_type = node["type"]
        node_name = node["name"]

        # Attributs optionnels
        attrs = {
            "label": node_name,
            "type": node_type,
            "access": node.get("access"),
            "exposed_as": node.get("exposed_as"),
        }
        G.add_node(node_id, **attrs)

        for child in node.get("children", []):
            child_id = child["id"]
            G.add_node(child_id)
            G.add_edge(node_id, child_id)
            build_graph_from_tree(child, G)

        return G

    def compute_positions(G: nx.DiGraph) -> dict:
        """
        Disposition hiérarchique homogène par niveau (BFS depuis root).
        Retourne {node_id: (x, y)}.
        """
        # Niveaux BFS
        levels = {}
        for node in nx.topological_sort(G):
            preds = list(G.predecessors(node))
            if not preds:
                levels[node] = 0
            else:
                levels[node] = max(levels[p] for p in preds) + 1

        # Groupement par niveau
        from collections import defaultdict
        level_nodes = defaultdict(list)
        for node, lvl in levels.items():
            level_nodes[lvl].append(node)

        # Calcul des positions — x = niveau, y = position dans le niveau
        pos = {}
        for lvl, nodes in level_nodes.items():
            n = len(nodes)
            for i, node in enumerate(nodes):
                pos[node] = (
                    lvl * 3,  # x — espacement horizontal
                    -(i - (n - 1) / 2) * 2  # y — centré verticalement
                )

        return pos

    # Couleurs et icônes par type de nœud
    NODE_STYLE = {
        "root": {"color": "#4A4E69", "symbol": "diamond", "size": 20},
        "file": {"color": "#3A86FF", "symbol": "square", "size": 16},
        "function": {"color": "#8338EC", "symbol": "circle", "size": 14},
        "table": {"color": "#FB5607", "symbol": "square", "size": 14},
        "field": {"color": "#06D6A0", "symbol": "circle", "size": 12},
        "role": {"color": "#FFB703", "symbol": "star", "size": 12},
    }

    ACCESS_COLOR = {
        "direct": "#06D6A0",
        "indirect": "#FF6B6B",
        None: "#06D6A0",
    }

    def build_figure(G: nx.DiGraph, pos: dict) -> go.Figure:
        """Construit la figure Plotly depuis le graphe et les positions."""

        # ── Edges ──────────────────────────────────────────────
        edge_x, edge_y = [], []
        for src, dst in G.edges():
            x0, y0 = pos[src]
            x1, y1 = pos[dst]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            mode="lines",
            line=dict(width=1, color="#AAAAAA"),
            hoverinfo="none",
        )

        # ── Nodes — un trace par type pour la légende ──────────
        node_traces = []
        from collections import defaultdict
        by_type = defaultdict(list)

        for node_id, attrs in G.nodes(data=True):
            ntype = attrs.get("type", "field")
            by_type[ntype].append((node_id, attrs))

        for ntype, items in by_type.items():
            style = NODE_STYLE.get(ntype, NODE_STYLE["field"])

            xs, ys, texts, hovers, colors = [], [], [], [], []
            for node_id, attrs in items:
                x, y = pos[node_id]
                xs.append(x)
                ys.append(y)
                texts.append(attrs.get("label", node_id))

                # Couleur selon accès pour les fields
                if ntype == "field":
                    colors.append(ACCESS_COLOR[attrs.get("access")])
                else:
                    colors.append(style["color"])

                # Tooltip
                hover = f"<b>{attrs.get('label', node_id)}</b><br>type: {ntype}"
                if attrs.get("access"):
                    hover += f"<br>access: {attrs['access']}"
                if attrs.get("exposed_as"):
                    hover += f"<br>exposed_as: {attrs['exposed_as']}"
                hovers.append(hover)

            node_traces.append(go.Scatter(
                x=xs, y=ys,
                mode="markers+text",
                name=ntype,
                marker=dict(
                    symbol=style["symbol"],
                    size=style["size"],
                    color=colors,
                    line=dict(width=1, color="#FFFFFF")
                ),
                text=texts,
                textposition="middle right",
                textfont=dict(size=10),
                hovertext=hovers,
                hoverinfo="text",
            ))

        fig = go.Figure(
            data=[edge_trace] + node_traces,
            layout=go.Layout(
                title="DAG — Arbre des droits d'accès",
                showlegend=True,
                hovermode="closest",
                margin=dict(l=20, r=20, t=50, b=20),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor="#1E1E2E",
                paper_bgcolor="#1E1E2E",
                font=dict(color="#FFFFFF"),
                legend=dict(
                    title="Type de nœud",
                    bgcolor="#2A2A3E",
                    bordercolor="#444",
                    borderwidth=1,
                )
            )
        )
        return fig

    @app.callback(
        Output(component_id='div_auth_tree_sqlglot', component_property='children'),
        Input(component_id='fake', component_property='value'),
        State(component_id='token', component_property='data')
    )
    def display_tree_sqlglot(user_id_fake, token):
        data = app14_check_tools.get_access_auth_tree_sqlglot(token)
        logging.info(data)

        # Vérification de la réponse
        if not data:
            return [html.Label("No data available")]

        tree = data
        # if not tree:
        #     logging.info("No data available")
        #     return [html.Label("No tree data")]

        try:
            # Construction du graphe
            G = build_graph_from_tree(tree)
            pos = compute_positions(G)
            fig = build_figure(G, pos)

            return [
                dcc.Graph(
                    figure=fig,
                    style={"height": "85vh"},
                    config={"scrollZoom": True, "displayModeBar": True}
                )
            ]

        except Exception as e:
            logging.info(f"Erreur construction DAG : {e}", exc_info=True)
            return [html.Label(f"Erreur : {e}")]
            #return [html.Label("No data available")]