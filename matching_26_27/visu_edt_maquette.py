# récupère les heures de maquette par module dans idu_maquette.json en affichant les heures de CM, TD et TP par module

import json
from pathlib import Path

MAQUETTE_PATH = Path(__file__).resolve().with_name("idu_maquette.json")


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

    with open("h_maquette.json", "wt+", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Fichier créé : h_maquette.json")

if __name__ == "__main__":
    afficher_heures_maquette()


# FULL IA
# compare pour chaque module les heures de maquette de CM, TD et TP avec l'emploi du temps
# import json
# from collections import defaultdict
# from pathlib import Path

# import matplotlib.pyplot as plt


# ROOT = Path(__file__).resolve().parent
# MAQUETTE_PATH = ROOT / "idu_maquette.json"
# SNAPSHOTS_PATH = ROOT / "scrapping" / "snapshots" / "IDU"
# COURSE_TYPES = ("CM", "TD", "TP")


# def iter_modules(nodes):
#     for node in nodes:
#         if node.get("type") == "module":
#             yield node
#         yield from iter_modules(node.get("modules", []))
#         yield from iter_modules(node.get("sous_modules", []))


# def module_code(code):
#     return str(code or "").split("_", maxsplit=1)[0].upper()


# def is_idu4_event(event):
#     return any(
#         group.get("filiere") == "IDU" and group.get("annee") == 4
#         for group in event.get("groupes", [])
#     )


# def cohort_groups(event):
#     return [
#         group
#         for group in event.get("groupes", [])
#         if group.get("filiere") == "IDU" and group.get("annee") == 4
#     ]


# def is_specific_cohort_group(group):
#     return bool(group.get("nom")) and (group.get("sous_groupe") or "").casefold() not in {
#         "",
#         "promo",
#     }


# def main():
#     maquette = json.loads(MAQUETTE_PATH.read_text(encoding="utf-8"))
#     parcours = [
#         item
#         for item in maquette.get("parcours", [])
#         if "alternance" not in item.get("nom", "").casefold()
#     ]
#     if len(parcours) != 1:
#         raise ValueError(
#             f"Un seul parcours IDU hors alternance est attendu dans {MAQUETTE_PATH}; "
#             f"{len(parcours)} trouvé(s)"
#         )

#     modules_by_code = defaultdict(list)
#     for semestre in parcours[0].get("semestres", []):
#         if semestre.get("numero") not in (7, 8):
#             continue
#         for ue in semestre.get("ue", []):
#             for module in iter_modules(ue.get("modules", [])):
#                 code = module_code(module.get("code"))
#                 if code:
#                     modules_by_code[code].append(module)
#     if not modules_by_code:
#         raise ValueError("Aucun module IDU des semestres 7 et 8 n'a été trouvé")

#     snapshots = sorted(SNAPSHOTS_PATH.glob("*/edt.json"))
#     if not snapshots:
#         raise FileNotFoundError(f"Aucun snapshot edt.json trouvé dans {SNAPSHOTS_PATH}")
#     edt_path = snapshots[-1]
#     edt = json.loads(edt_path.read_text(encoding="utf-8"))

#     plan = {}
#     labels = {}
#     for code, modules in modules_by_code.items():
#         plan[code] = {
#             kind.casefold(): sum(
#                 float(module["heures"][kind.casefold()])
#                 for module in modules
#                 if module.get("heures", {}).get(kind.casefold()) is not None
#             )
#             for kind in COURSE_TYPES
#         }
#         titles = list(dict.fromkeys(module.get("titre", "") for module in modules if module.get("titre")))
#         labels[code] = f"{code} — {' / '.join(titles)}" if titles else code

#     sessions_by_course = defaultdict(list)
#     seen_sessions = set()
#     matched_events = 0
#     for event in edt.get("evenements", []):
#         kind = event.get("type_cours")
#         code = module_code(event.get("code_matiere"))
#         if (
#             not is_idu4_event(event)
#             or kind not in COURSE_TYPES
#             or code not in modules_by_code
#         ):
#             continue

#         session = (code, kind, event.get("debut"), event.get("fin"))
#         if session in seen_sessions:
#             continue
#         seen_sessions.add(session)
#         sessions_by_course[(code, kind)].append(
#             (float(event.get("duree_minutes") or 0) / 60, cohort_groups(event))
#         )
#         matched_events += 1

#     if not matched_events:
#         raise ValueError(
#             f"Aucun cours CM, TD ou TP d'IDU-4 ne correspond aux modules "
#             f"des semestres 7 et 8 dans {edt_path}"
#         )

#     schedule = {
#         code: {kind.casefold(): 0.0 for kind in COURSE_TYPES}
#         for code in modules_by_code
#     }
#     for (code, kind), sessions in sessions_by_course.items():
#         subgroup_names = {
#             group["nom"]
#             for _, groups in sessions
#             for group in groups
#             if is_specific_cohort_group(group)
#         }
#         hours_by_group = defaultdict(float)
#         for duration, groups in sessions:
#             specific_groups = {
#                 group["nom"]
#                 for group in groups
#                 if is_specific_cohort_group(group)
#             }
#             target_groups = specific_groups or subgroup_names or {"IDU-4-Promo"}
#             for group_name in target_groups:
#                 hours_by_group[group_name] += duration
#         schedule[code][kind.casefold()] = max(hours_by_group.values(), default=0.0)

#     rows = sorted(modules_by_code)
#     figure_height = max(10, len(rows) * 0.38)
#     fig, axes = plt.subplots(
#         nrows=len(COURSE_TYPES),
#         figsize=(16, figure_height),
#         sharey=True,
#     )
#     positions = list(range(len(rows)))
#     bar_height = 0.36

#     for axis, kind in zip(axes, COURSE_TYPES):
#         key = kind.casefold()
#         planned = [plan[code][key] for code in rows]
#         scheduled = [schedule[code][key] for code in rows]
#         axis.barh(
#             [position - bar_height / 2 for position in positions],
#             planned,
#             height=bar_height,
#             label="Maquette",
#             color="#4C78A8",
#         )
#         axis.barh(
#             [position + bar_height / 2 for position in positions],
#             scheduled,
#             height=bar_height,
#             label="Emploi du temps",
#             color="#F58518",
#         )
#         axis.set_title(f"{kind} — maquette et emploi du temps")
#         axis.set_xlabel("Heures")
#         axis.grid(axis="x", alpha=0.25)
#         axis.set_yticks(positions, labels=[labels[code] for code in rows], fontsize=7)
#         axis.invert_yaxis()

#     axes[0].legend(loc="best")
#     export_date = edt.get("meta", {}).get("horodatage_export", edt_path.parent.name)
#     fig.suptitle(
#         f"IDU-4 — semestres 7 et 8 — heures maquette / EDT par sous-groupe ({export_date})",
#         fontsize=14,
#     )
#     fig.tight_layout(rect=(0, 0, 1, 0.99))

#     output_path = ROOT / "visu_edt_maquette.png"
#     fig.savefig(output_path, dpi=150, bbox_inches="tight")
#     print(f"Comparaison enregistrée dans {output_path}")
#     print(f"Snapshot utilisé : {edt_path}")
#     print(f"Événements CM/TD/TP comparés : {matched_events}")
#     print("Pour les séances en sous-groupes, l'EDT affiche le total du sous-groupe le plus chargé.")
#     plt.show()


# if __name__ == "__main__":
#     main()