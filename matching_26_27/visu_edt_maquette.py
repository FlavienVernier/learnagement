# récupère les heures de maquette par module dans idu_maquette.json en affichant les heures de CM, TD et TP par module

import json
from pathlib import Path

MAQUETTE_PATH = Path(__file__).resolve().parents[1] / "scrapping" / "scrapped_data" / "idu_maquette.json"

def afficher_heures_maquette():
    data = []
    maquette = json.loads(MAQUETTE_PATH.read_text(encoding="utf-8"))
    for parcours in maquette.get("parcours", []):
        for semestre in parcours.get("semestres", []):
            for ue in semestre.get("ue", []):
                for module in ue.get("modules", []):
                    if module.get("type") == "module":
                        heures = module.get("heures", {})
                        data.append({"module": module.get("code"), "heures": module.get("heures", {})})

    output_path = Path(__file__).resolve().parents[1] / "scrapping" / "scrapped_data" / "h_maquette.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Fichier créé : h_maquette.json")

if __name__ == "__main__":
    afficher_heures_maquette()
