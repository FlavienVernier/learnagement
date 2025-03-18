import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import colorsys
import matplotlib.colors as mcolors#
import mysql
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
#cur.execute("SELECT * FROM VIEW_graphe_dependances")
cur.execute("SELECT `id_sequence_prev`, `id_sequence_next`, LNM_seanceType.type, MAQUETTE_module.code_module, MAQUETTE_module.nom, MAQUETTE_module_sequence.commentaire \
FROM `MAQUETTE_dependance_sequence` \
JOIN MAQUETTE_module_sequence on MAQUETTE_module_sequence.id_module_sequence = MAQUETTE_dependance_sequence.id_sequence_prev \
JOIN MAQUETTE_module_sequencage ON MAQUETTE_module_sequencage.id_module_sequencage = MAQUETTE_module_sequence.id_module_sequencage \
JOIN MAQUETTE_module ON MAQUETTE_module.id_module = MAQUETTE_module_sequencage.id_module \
JOIN LNM_seanceType ON LNM_seanceType.id_seance_type = MAQUETTE_module_sequencage.id_seance_type \
WHERE 1;")


rows = cur.fetchall()

# Créer le dag
edges = [(row[0], row[1]) for row in rows if row[1] is not None]
nodes = set([row[0] for row in rows]) | set([row[1] for row in rows if row[1] is not None])
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Récupérer les informations des nœuds
node_info = {row[0]: {
    'type': row[2],
    'code': row[3],
    'nom_module': row[4],
    'nom_sequence': row[5]
} for row in rows}


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

# Tracés des nœuds avec les infos
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
        label = f"{node_data['type']}-{node_data['code']}"
        hover = f"{node_data['type']} - {node_data['code']}\n{node_data['nom_module']}\n{node_data['nom_sequence'] if node_data['nom_sequence'] else ''}"
    else:
        print(f"Mince ! Le noeud {node} n'a pas de données associées !")
        label = "Unknown"
        hover = "No data"
    node_text.append(label)
    node_hovertext.append(hover)

# Fonction pour assombrir une couleur (purement pour l'esthétique lol)
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

# Assombrir les couleurs des contours des noeuds parce que c'est stylé
dark_node_color_values = [darken_color(color) for color in node_color_values]


app11_layout = html.Div([
    html.H1("Dépendance des cours",
            style={'font-family': 'verdana'}
            ),
    dcc.Graph(id='dag', style={'marginTop': '30px', 'height':1000})
])

def register_callbacks(app):

    @app.callback(
            Output('dag', 'figure'),
            Input('dag', 'id') 
        )
    
    def update_graph(_):
        # tracer les noeuds avec les infos et les couleurs (contours assombris)
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            text=node_text,
            textposition='top center',
            hovertext=node_hovertext,
            hoverinfo='text',
            marker=dict(
                size=10,
                color=node_color_values,
                line=dict(width=0.5, color=dark_node_color_values)
            )
        )

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=0, l=0, r=0, t=0),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False),
                            annotations=annotations
                        ))

        return fig
