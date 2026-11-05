from pathlib import Path
import json

import matplotlib.pyplot as plt

json_path = Path(__file__).with_name("learnagement.json")
with json_path.open("r", encoding="utf-8") as f:
    export = json.load(f)

modules = next(
    (
        table["data"]
        for table in export
        if table.get("type") == "table" and table.get("name") == "MAQUETTE_module"
    ),
    None,
)
if modules is None:
    raise ValueError(f"La table MAQUETTE_module est introuvable dans {json_path}")

heures_par_type = {
    "CM": "hCM",
    "TD": "hTD",
    "TP": "hTP",
    "Projet": "hPROJ",
    "Personnel": "hPersonnelle",
}
categories = list(heures_par_type)
valeurs = [
    sum(float(module.get(champ) or 0) for module in modules)
    for champ in heures_par_type.values()
]

if not any(valeurs):
    raise ValueError("Aucune heure de module n'a été trouvée dans MAQUETTE_module")

plt.figure(figsize=(8, 5))
plt.bar(categories, valeurs, color="skyblue")

plt.title("Répartition des heures")
plt.xlabel("Type d'enseignement")
plt.ylabel("Nombre d'heures")

for i, valeur in enumerate(valeurs):
    plt.text(i, valeur + 1, f"{valeur:g}", ha="center")

plt.tight_layout()
plt.savefig(Path(__file__).with_name("graph.png"))
plt.show()