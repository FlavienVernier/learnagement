import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import colorsys
import matplotlib.colors as mcolors
import mysql.connector
from dash import dcc, html
from dash.dependencies import Input, Output

# variables de configuration
color_mode = "module"  # "groupe" ou "module"
edge_color = "#555"
node_radius = 0.05

# Lire les informations de connexion depuis logs_db.txt
with open('logs_db.txt', 'r') as file:
    lines = file.readlines()
    user = lines[0].strip()
    password = lines[1].strip()
    host = lines[2].strip()
    port = lines[3].strip()
    database = lines[4].strip()

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
cur.execute("SELECT * FROM VIEW_graphe_dependances_modules")

rows = cur.fetchall()

# Créer le dag
nodes = set([row[1] for row in rows]) | set([row[2] for row in rows if row[2] is not None and row[1] != row[2]])
edges = [(row[1], row[2]) for row in rows if row[2] is not None and row[1] != row[2]]
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Infos des noeuds
node_info = {}
for row in rows:
    if row[1] not in node_info:
        node_info[row[1]] = {'code': row[1], 'module': row[0], 'nbDependance': row[3] if row[3] is not None else 0}
    else:
        node_info[row[1]]['nbDependance'] += row[3]

# Définir les couleurs des noeuds en fonction du mode de coloration chosii 
if color_mode == "groupe":
    # Coloration par groupe (composantes connexes)
    groups = list(nx.connected_components(G.to_undirected()))
    group_map = {node: i for i, group in enumerate(groups) for node in group}
    node_colors = [group_map[node] for node in nodes]
    color_palette = px.colors.qualitative.Set3
    color_map = {i: color_palette[i % len(color_palette)] for i in set(node_colors)}
    node_color_values = [color_map[group_map[node]] for node in nodes]

elif color_mode == "module":
    # Coloration par code module
    unique_codes = {node_info[node]['code'] for node in nodes if node in node_info}
    code_map = {code: i for i, code in enumerate(unique_codes)}
    color_palette = px.colors.qualitative.Pastel
    color_map = {i: color_palette[i % len(color_palette)] for i in set(code_map.values())}
    node_color_values = [color_map[code_map[node_info[node]['code']]] if node in node_info else "#CCCCCC" for node in nodes]

# Calcul des positions des nœuds avec un algo de disposition
pos = nx.spring_layout(G)  # en vrai on peut le remplacer par d'autres algos

edge_x = []
edge_y = []
arrows_x = []
arrows_y = []
annotations = []

for edge in edges:
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

    # Ajouter des coordonnées pour les flèches
    arrows_x.append((x0 + x1) / 2)
    arrows_y.append((y0 + y1) / 2)

    # Ajouter des annotations pour les flèches
    annotations.append(
        dict(
            ax=x0,
            ay=y0,
            axref='x',
            ayref='y',
            x=x1,
            y=y1,
            xref='x',
            yref='y',
            showarrow=True,
            arrowhead=1,
            arrowsize=3,
            arrowwidth=0.6,
            arrowcolor=edge_color
        )
    )

# Tracés des arêtes
edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=1, color=edge_color),
    hoverinfo='none'
)

# Tracés des nœuds avec les couleurs et le code en label et le code - nom en hover
node_x = []
node_y = []
node_text = []
node_hovertext = []
for node in nodes:
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    if node in node_info:
        node_data = node_info[node]
        label = f"{node_data['code']}"
        hover = f"{node_data['code']} - {node_data['module']} ({node_data['nbDependance']} dépendances)"
    else:
        print(f"Mince ! Le noeud {node} n'a pas de données associées !")
        label = "Unknown"
        hover = "No data"
    node_text.append(label)
    node_hovertext.append(hover)

def darken_color(color, factor=0.3):
    # Convertir la couleur d'un string ('rgb(255, 255, 255)') à un tuple (1.0, 1.0, 1.0)
    if color.startswith('rgb'):
        color = color.replace('rgb(', '').replace(')', '')
        rgb = tuple(int(c) / 255.0 for c in color.split(','))
    else:
        rgb = mcolors.to_rgb(color)
    hls = colorsys.rgb_to_hls(*rgb) # Convertir RGB en HLS (Hue, Lightness, Saturation)
    darkened_hls = (hls[0], max(0, min(1, hls[1] * (1 - factor))), hls[2]) # Assombrir la luminosité
    darkened_rgb = colorsys.hls_to_rgb(*darkened_hls) # Et on repasse en RGB
    return mcolors.to_hex(darkened_rgb)

app12_layout = html.Div([
    html.H1("Dépendance des modules",
            style={'font-family': 'verdana'}
            ),
    dcc.Graph(id='dag_module', style={'marginTop': '30px'})
])

def register_callbacks(app):

    @app.callback(
            Output('dag_module', 'figure'),
            Input('dag_module', 'id') 
        )
    
    def update_graph(_):
        # Assombrir les couleurs des nœuds pour les bordures
        node_border_colors = [darken_color(color) for color in node_color_values]

        # Tracés des nœuds
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            text=node_text,
            textposition='top center',
            hoverinfo='text',
            hovertext=node_hovertext,
            marker=dict(
                color=node_color_values,
                size=[(10 + node_info[node]['nbDependance']) * node_radius * 50 for node in nodes],
                line=dict(width=0.5, color=node_border_colors)
            )
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=annotations,
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                        ))

        return fig