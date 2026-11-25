from dash import Dash, dcc, html
import plotly.graph_objects as go

from get_lessons import get_lessons
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

evenements_edt = get_lessons(maquette_module["code"])
if not evenements_edt:
    raise ValueError(
        f"Aucun événement EDT trouvé pour {maquette_module['code']}."
    )

heures_edt = {type_cours: 0.0 for type_cours in types_cours}

for evenement in evenements_edt:
    type_cours = evenement.get("type_cours")
    duree_minutes = evenement.get("duree_minutes")

    if type_cours not in heures_edt:
        raise ValueError(f"Type de cours EDT inconnu : {type_cours!r}")
    if duree_minutes is None:
        raise ValueError(f"Durée manquante pour l'événement EDT : {evenement}")

    heures_edt[type_cours] += float(duree_minutes) / 60

figure = go.Figure()
figure.add_trace(
    go.Bar(name="Maquette", x=types_cours, y=heures_prevues)
)
figure.add_trace(
    go.Bar(
        name="Séances entrées par la professeure",
        x=types_cours,
        y=heures_professeure,
    )
)
figure.add_trace(
    go.Bar(
        name="EDT",
        x=types_cours,
        y=[heures_edt[type_cours] for type_cours in types_cours],
    )
)
figure.update_layout(
    title="Comparaison des heures par type de cours",
    xaxis_title="Type de cours",
    yaxis_title="Heures",
    barmode="group",
)

app = Dash(__name__)
app.layout = html.Main([
    html.H1("Comparaison Maquette / Professeur / EDT"),
    html.P(f"Professeur : {prof['prenom']} {prof['nom']}"),
    html.P(f"Module : {maquette_module['code']} — {maquette_module['titre']}"),
    dcc.Graph(figure=figure),
])

if __name__ == "__main__":
    app.run(debug=True, port=8052)