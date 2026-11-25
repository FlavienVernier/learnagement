from dash import Dash, dcc, html
import plotly.graph_objects as go

from matching_maq_maqprof import (
    heures_maquette,
    heures_prof,
    maquette_module,
    prof,
)

types_cours = ["CM", "TD", "TP"]
heures_prevues = [
    float(heures_maquette.get(type_cours.lower()) or 0)
    for type_cours in types_cours
]
heures_professeure = [
    float(heures_prof[type_cours])
    for type_cours in types_cours
]

figure = go.Figure()
figure.add_trace(go.Bar(name="Maquette", x=types_cours, y=heures_prevues))
figure.add_trace(
    go.Bar(name="Séances attribuées à la professeure",
           x=types_cours, y=heures_professeure)
)
figure.update_layout(
    title="Heures par type de cours",
    xaxis_title="Type de cours",
    yaxis_title="Heures",
    barmode="group",
)

app = Dash(__name__)
app.layout = html.Main([
    html.H1("Comparaison avec la maquette"),
    html.P(f"{prof['prenom']} {prof['nom']} — {maquette_module['titre']}"),
    dcc.Graph(figure=figure),
])

if __name__ == "__main__":
    app.run(debug=True, port=8051)