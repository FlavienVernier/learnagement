
import json
from pathlib import Path

# exemple d'utilisation : donner le code d'un module à l'une des versions des fonctions
def adjust_name_module(name_module):
    """
    name_module : string, the code name of a module, example : "INFO732_IDU" (name taken from the code used in idu_maquette.json)
    Returns the appropriate name to search through edt.json, example : "INFO732"
    """
    if name_module.endswith("_IDU"):
        return name_module.replace("_IDU", "")
    elif name_module.endswith("_PACY"):
        return name_module.replace("_PACY", "")
    
#name_module = adjust_name_module("INFO732_IDU") # exemple

snapshots_path = Path(__file__).resolve().parents[2] / "learnagement" / "scrapping" / "snapshots" / "IDU"
path_edt_json = sorted(snapshots_path.glob("*/edt.json"))[-1]

#### chercher tous les cours du module demandé dans le fichier edt.json
def get_lessons(name_maq):
    name_maq = adjust_name_module(name_maq)
    lessons=[]

    edt = json.loads(path_edt_json.read_text(encoding="utf-8"))

    for evenement in edt.get("evenements", []):
            if evenement.get("code_matiere") == name_maq:
                lesson = {"type_cours": evenement.get("type_cours"),
                          "debut": evenement.get("debut"),
                          "duree_minutes": evenement.get("duree_minutes"),}
                lessons.append(lesson)
    return lessons

#print(get_lessons(name_module))