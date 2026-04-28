"""
Outils disponibles pour le chatbot APC.
Chaque outil correspond à une fonction Python qui interroge la BD via l'API,
et à un schéma JSON que l'API Gemini utilise pour savoir quand l'appeler.
"""
import pandas as pd
from .apc20_heatmap_apc_tools import (
    get_apc_competences,
    get_apc_niveaux,
    get_apc_apprentissages,
    get_apc_ac_modules,
    get_apc_modules,
)


# ── Schémas des outils pour l'API Gemini ──────────────────────────
# Les types sont en MAJUSCULES (format JSON Schema Gemini)

GEMINI_TOOLS = [
    {
        "name": "lister_modules",
        "description": (
            "Liste tous les modules de la formation avec leur identifiant, code et nom. "
            "Utilise cet outil pour connaître les modules disponibles ou pour trouver "
            "l'identifiant d'un module avant d'appeler un autre outil."
        ),
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "lister_competences",
        "description": "Liste toutes les compétences du référentiel APC avec leur code et libellé.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "lister_ac",
        "description": (
            "Liste tous les apprentissages critiques (AC) du référentiel avec leur libellé, "
            "la compétence associée et le niveau (N1, N2, N3). "
            "Utilise cet outil pour trouver l'identifiant d'un AC."
        ),
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "lister_ac_du_module",
        "description": (
            "Liste les apprentissages critiques couverts par un module spécifique, "
            "avec le type de lien (Requis, Recommandé, Complémentaire), "
            "la compétence associée et le niveau."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "id_module": {
                    "type": "number",
                    "description": "Identifiant numérique du module (obtenu via lister_modules)",
                }
            },
            "required": ["id_module"],
        },
    },
    {
        "name": "lister_modules_dun_ac",
        "description": (
            "Liste tous les modules qui couvrent un apprentissage critique donné, "
            "avec le type de lien (Requis, Recommandé, Complémentaire)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "id_ac": {
                    "type": "number",
                    "description": "Identifiant numérique de l'apprentissage critique (obtenu via lister_ac)",
                }
            },
            "required": ["id_ac"],
        },
    },
    {
        "name": "ac_sans_module_requis",
        "description": (
            "Retourne la liste des apprentissages critiques qui n'ont aucun module "
            "avec un lien de type 'Requis'. Ce sont les trous du référentiel APC."
        ),
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "modules_sans_ac_requis",
        "description": (
            "Retourne la liste des modules qui n'ont aucun apprentissage critique "
            "avec un lien de type 'Requis'. Ce sont les modules à ancrage APC faible."
        ),
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "statistiques_globales",
        "description": (
            "Retourne des statistiques globales sur le référentiel APC : "
            "nombre de modules, compétences, AC, taux de couverture, nombre de trous."
        ),
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "couverture_competence",
        "description": (
            "Analyse la couverture d'une compétence spécifique : pour chaque niveau "
            "(N1, N2, N3), liste les AC et combien de modules les couvrent."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "code_competence": {
                    "type": "string",
                    "description": "Code de la compétence (ex: COMP_IDU1, COMP_IDU2...)",
                }
            },
            "required": ["code_competence"],
        },
    },
]


# ── Construction du DataFrame principal ───────────────────────────

def _build_df_main(token):
    df_comp  = get_apc_competences(token)
    df_niv   = get_apc_niveaux(token)
    df_ac    = get_apc_apprentissages(token)
    df_acmod = get_apc_ac_modules(token)
    df_mod   = get_apc_modules(token)

    df_base = (
        df_ac
        .merge(df_niv,  on="id_niveau",     how="left")
        .merge(df_comp, on="id_competence", how="left")
    )

    if not df_mod.empty and "id_module" in df_mod.columns:
        df_acmod_full = df_acmod.merge(df_mod, on="id_module", how="left")
    else:
        df_acmod_full = df_acmod.copy()

    df_main = df_base.merge(df_acmod_full, on="id_apprentissage_critique", how="left")
    df_main["id_module"] = pd.to_numeric(
        df_main["id_module"] if "id_module" in df_main.columns else 0,
        errors="coerce",
    ).fillna(0)
    return df_main, df_mod, df_comp


# ── Routeur d'exécution ───────────────────────────────────────────

def execute_tool(name: str, inputs: dict, token: str) -> str:
    try:
        if name == "lister_modules":
            return _lister_modules(token)
        elif name == "lister_competences":
            return _lister_competences(token)
        elif name == "lister_ac":
            return _lister_ac(token)
        elif name == "lister_ac_du_module":
            return _lister_ac_du_module(token, inputs["id_module"])
        elif name == "lister_modules_dun_ac":
            return _lister_modules_dun_ac(token, inputs["id_ac"])
        elif name == "ac_sans_module_requis":
            return _ac_sans_module_requis(token)
        elif name == "modules_sans_ac_requis":
            return _modules_sans_ac_requis(token)
        elif name == "statistiques_globales":
            return _statistiques_globales(token)
        elif name == "couverture_competence":
            return _couverture_competence(token, inputs["code_competence"])
        else:
            return f"Outil inconnu : {name}"
    except Exception as e:
        return f"Erreur lors de l'exécution de l'outil '{name}' : {e}"


# ── Implémentations ───────────────────────────────────────────────

def _lister_modules(token):
    df = get_apc_modules(token)
    if df.empty:
        return "Aucun module trouvé dans la base de données."
    rows = []
    for _, r in df.iterrows():
        code = r.get("code_module", f"M{r['id_module']}")
        nom  = r.get("nom", "")
        rows.append(f"- id={int(r['id_module'])} | {code} — {nom}")
    return f"{len(df)} modules disponibles :\n" + "\n".join(rows)


def _lister_competences(token):
    df = get_apc_competences(token)
    if df.empty:
        return "Aucune compétence trouvée."
    rows = [
        f"- {r['code_competence']} : {r.get('libelle_competence', '')}"
        for _, r in df.iterrows()
    ]
    return f"{len(df)} compétences :\n" + "\n".join(rows)


def _lister_ac(token):
    df_ac  = get_apc_apprentissages(token)
    df_niv = get_apc_niveaux(token)
    df_com = get_apc_competences(token)
    df = (
        df_ac
        .merge(df_niv, on="id_niveau",     how="left")
        .merge(df_com, on="id_competence", how="left")
    )
    if df.empty:
        return "Aucun apprentissage critique trouvé."
    rows = []
    for _, r in df.sort_values(["code_competence", "niveau"]).iterrows():
        rows.append(
            f"- id={int(r['id_apprentissage_critique'])} | "
            f"{r['code_competence']} N{int(r['niveau'])} : {r['libelle_apprentissage']}"
        )
    return f"{len(df)} apprentissages critiques :\n" + "\n".join(rows)


def _lister_ac_du_module(token, id_module):
    df_main, _, _ = _build_df_main(token)
    df = df_main[df_main["id_module"] == float(id_module)].drop_duplicates("id_apprentissage_critique")
    if df.empty:
        return f"Aucun AC trouvé pour le module id={id_module}."
    mod_name = df.iloc[0].get("nom", f"Module {id_module}")
    rows = []
    for _, r in df.sort_values(["code_competence", "niveau"]).iterrows():
        lien = r.get("type_lien", "?")
        rows.append(f"- [{lien}] {r['code_competence']} N{int(r['niveau'])} : {r['libelle_apprentissage']}")
    return f"Module '{mod_name}' — {len(df)} AC couverts :\n" + "\n".join(rows)


def _lister_modules_dun_ac(token, id_ac):
    df_main, _, _ = _build_df_main(token)
    df = df_main[df_main["id_apprentissage_critique"] == float(id_ac)].drop_duplicates("id_module")
    df = df[df["id_module"] != 0]
    if df.empty:
        return f"Aucun module ne couvre l'AC id={id_ac}."
    ac_label = df.iloc[0].get("libelle_apprentissage", f"AC {id_ac}")
    rows = []
    for _, r in df.iterrows():
        nom  = r.get("nom", f"Module {int(r['id_module'])}")
        code = r.get("code_module", "")
        lien = r.get("type_lien", "?")
        rows.append(f"- [{lien}] {code} — {nom}")
    return f"AC '{ac_label}' couvert par {len(df)} module(s) :\n" + "\n".join(rows)


def _ac_sans_module_requis(token):
    df_main, _, _ = _build_df_main(token)
    ac_requis = set(df_main[df_main["type_lien"] == "Requis"]["id_apprentissage_critique"])
    all_acs   = df_main[
        ["id_apprentissage_critique", "libelle_apprentissage", "code_competence", "niveau"]
    ].drop_duplicates("id_apprentissage_critique")
    orphans   = all_acs[~all_acs["id_apprentissage_critique"].isin(ac_requis)]
    if orphans.empty:
        return "Tous les AC ont au moins un module avec lien 'Requis'. Aucun trou détecté."
    rows = []
    for _, r in orphans.sort_values(["code_competence", "niveau"]).iterrows():
        rows.append(f"- {r['code_competence']} N{int(r['niveau'])} : {r['libelle_apprentissage']}")
    return f"{len(orphans)} AC sans module 'Requis' :\n" + "\n".join(rows)


def _modules_sans_ac_requis(token):
    df_main, df_mod, _ = _build_df_main(token)
    mod_requis  = set(df_main[df_main["type_lien"] == "Requis"]["id_module"])
    all_modules = df_main[df_main["id_module"] != 0]["id_module"].unique()
    orphans     = [m for m in all_modules if m not in mod_requis]
    if not orphans:
        return "Tous les modules ont au moins un AC avec lien 'Requis'."
    rows = []
    for m in sorted(orphans):
        row = df_mod[df_mod["id_module"] == m] if not df_mod.empty else pd.DataFrame()
        if not row.empty:
            nom  = row.iloc[0].get("nom", f"Module {int(m)}")
            code = row.iloc[0].get("code_module", "")
            rows.append(f"- {code} — {nom}")
        else:
            rows.append(f"- Module {int(m)}")
    return f"{len(orphans)} module(s) sans AC 'Requis' :\n" + "\n".join(rows)


def _statistiques_globales(token):
    df_main, _, df_comp = _build_df_main(token)
    nb_modules  = int(df_main[df_main["id_module"] != 0]["id_module"].nunique())
    nb_ac_total = int(df_main["id_apprentissage_critique"].nunique())
    nb_comp     = len(df_comp)
    nb_requis   = int(df_main[df_main["type_lien"] == "Requis"]["id_apprentissage_critique"].nunique())
    pct_requis  = round(nb_requis / nb_ac_total * 100) if nb_ac_total else 0

    ac_requis_set   = set(df_main[df_main["type_lien"] == "Requis"]["id_apprentissage_critique"])
    nb_ac_orphelins = nb_ac_total - len(ac_requis_set)

    mod_requis_set   = set(df_main[df_main["type_lien"] == "Requis"]["id_module"])
    all_mods         = df_main[df_main["id_module"] != 0]["id_module"].unique()
    nb_mod_orphelins = len([m for m in all_mods if m not in mod_requis_set])

    return (
        f"Statistiques globales du référentiel APC :\n"
        f"- Compétences : {nb_comp}\n"
        f"- Modules : {nb_modules}\n"
        f"- Apprentissages critiques (AC) : {nb_ac_total}\n"
        f"- AC ayant au moins un lien 'Requis' : {nb_requis} ({pct_requis}%)\n"
        f"- AC sans aucun lien 'Requis' (trous) : {nb_ac_orphelins}\n"
        f"- Modules sans AC 'Requis' : {nb_mod_orphelins}"
    )


def _couverture_competence(token, code_competence):
    df_main, _, _ = _build_df_main(token)
    df = df_main[df_main["code_competence"] == code_competence]
    if df.empty:
        return f"Compétence '{code_competence}' non trouvée ou aucune donnée disponible."
    rows = [f"Couverture de la compétence {code_competence} :"]
    for niveau in sorted(df["niveau"].dropna().unique()):
        df_niv = df[df["niveau"] == niveau].drop_duplicates("id_apprentissage_critique")
        rows.append(f"\n  Niveau N{int(niveau)} — {len(df_niv)} AC :")
        for _, r in df_niv.iterrows():
            nb_modules = df_main[
                (df_main["id_apprentissage_critique"] == r["id_apprentissage_critique"]) &
                (df_main["id_module"] != 0)
            ]["id_module"].nunique()
            rows.append(f"    • {r['libelle_apprentissage']} ({nb_modules} module(s))")
    return "\n".join(rows)
