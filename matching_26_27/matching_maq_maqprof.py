import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "learnagement.json"
MAQUETTE_PATH = ROOT / "scrapping" / "scrapped_data" / "idu_maquette.json"

# PROF_ID = "16"
# DB_MODULE_CODE = "INFO731_IDU"
# MAQUETTE_MODULE_CODE = "INFO731_IDU"

PROF_ID = "8"
DB_MODULE_CODE = "INFO732"
MAQUETTE_MODULE_CODE = "INFO732_IDU"

with DB_PATH.open(encoding="utf-8") as f:
    export = json.load(f)

tables = {
    table["name"]: table["data"]
    for table in export
    if table.get("type") == "table"
}

with MAQUETTE_PATH.open(encoding="utf-8") as f:
    maquette = json.load(f)

prof = next(
    (row for row in tables["LNM_enseignant"]
     if row["id_enseignant"] == PROF_ID),
    None,
)
db_module = next(
    (row for row in tables["MAQUETTE_module"]
     if row["code_module"] == DB_MODULE_CODE),
    None,
)

maquette_module = next(
    (
        module
        for parcours in maquette.get("parcours", [])
        for semestre in parcours.get("semestres", [])
        for ue in semestre.get("ue", [])
        for module in ue.get("modules", [])
        if module.get("code") == MAQUETTE_MODULE_CODE
    ),
    None,
)

if prof is None or db_module is None or maquette_module is None:
    raise ValueError("Professeur ou module introuvable dans les fichiers JSON.")
code_base = db_module["code_module"].strip().upper()
code_maquette = maquette_module["code"].strip().upper()

if code_maquette != code_base and not code_maquette.startswith(code_base + "_"):
    raise ValueError(
        f"Les codes ne correspondent pas : {code_base} / {code_maquette}"
    )

sequences = {
    row["id_module_sequence"]: row
    for row in tables["MAQUETTE_module_sequence"]
}
sequencages = {
    row["id_module_sequencage"]: row
    for row in tables["MAQUETTE_module_sequencage"]
}
types_seance = {
    row["id_seance_type"]: row["type"]
    for row in tables["LNM_seance_type"]
}

heures_prof = {"CM": 0.0, "TD": 0.0, "TP": 0.0}

for session in tables["CLASS_session"]:
    if session.get("id_enseignant") != PROF_ID:
        continue

    sequence = sequences.get(session.get("id_module_sequence"))
    if sequence is None:
        continue

    sequencage = sequencages.get(sequence.get("id_module_sequencage"))
    if sequencage is None or sequencage.get("id_module") != db_module["id_module"]:
        continue

    type_cours = types_seance.get(sequencage.get("id_seance_type"))
    if type_cours in heures_prof:
        heures_prof[type_cours] += float(sequencage["duree_h"])

heures_maquette = maquette_module.get("heures", {})

print(f"Professeure : {prof['prenom']} {prof['nom']} (id {PROF_ID})")
print(f"Module maquette : {maquette_module['code']} — {maquette_module['titre']}")

for type_cours, cle_maquette in [
    ("CM", "cm"),
    ("TD", "td"),
    ("TP", "tp"),
]:
    attendu = float(heures_maquette.get(cle_maquette) or 0)
    attribue = heures_prof[type_cours]
    print(
        f"{type_cours} : maquette={attendu:g} h, "
        f"attribué à la prof={attribue:g} h, "
        f"écart={attribue - attendu:+g} h"
    )