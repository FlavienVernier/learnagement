### pour l'instant fonctionne en déplaçant à la main idu_maquette.json et h_maquette.json dans /matching_26_27
"""
Récupérer les heures de maquette d'un module spécifique à partir de son code
Renvoie un json de format : {"cm", "td", "tp", "contact_total"}
"""

import json
from pathlib import Path

# exemple d'utilisation : donner le code d'un module à l'une des versions des fonctions
name_module = "MATH501_PACY"

path_maq_json = Path(__file__).resolve().with_name("idu_maquette.json")
path_h_json = Path(__file__).resolve().with_name("h_maquette.json")

#### version 1 : chercher une maquette à partir du fichier json complet des maquettes idu_maquette.json
def get_maquette_verDirect(name_maq):
    maquette = json.loads(path_maq_json.read_text(encoding="utf-8"))
    for parcours in maquette.get("parcours", []):
            for semestre in parcours.get("semestres", []):
                for ue in semestre.get("ue", []):
                    for module in ue.get("modules", []):
                        if module.get("type") == "module" and module.get("code") == name_maq:
                            return module.get("heures", {})
    return None

print(get_maquette_verDirect(name_module))


#### version 2 : chercher une maquette à partir du fichier json simplifié par visu_edt_maquette.py
def get_maquette_verCompiled(name_maq):

    maquette = json.loads(path_h_json.read_text(encoding="utf-8"))
    for module in maquette:
        if module.get("module") == name_maq:
            return module.get("heures")
    return None

#print(get_maquette_verCompiled(name_module))
