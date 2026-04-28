import logging
import pandas as pd
from dash import Input, Output

from .apc20_heatmap_apc_tools import (
    get_apc_competences,
    get_apc_niveaux,
    get_apc_apprentissages,
    get_apc_ac_modules,
    get_apc_modules,
    get_apc_composantes,
)


def register_ens_data_loader(app):

    @app.callback(
        Output("apc-ens-raw-store", "data"),
        Input("token", "data"),
        prevent_initial_call=False,
    )
    def load_ens_data(token):
        if not token or token == "none":
            logging.info("[apc20_ens_data_loader] token absent, chargement ignoré")
            return None

        try:
            df_competences = get_apc_competences(token)
            df_niveaux = get_apc_niveaux(token)
            df_apprentissages = get_apc_apprentissages(token)
            df_ac_modules_raw = get_apc_ac_modules(token)
            df_modules = get_apc_modules(token)
            df_composantes = get_apc_composantes(token)

            df_base = (
                df_apprentissages
                .merge(df_niveaux, on="id_niveau", how="left")
                .merge(df_competences, on="id_competence", how="left")
            )

            if not df_modules.empty and "id_module" in df_modules.columns:
                df_ac_mod_full = df_ac_modules_raw.merge(df_modules, on="id_module", how="left")
            else:
                df_ac_mod_full = df_ac_modules_raw.copy()

            df_main = df_base.merge(df_ac_mod_full, on="id_apprentissage_critique", how="left")

            df_main["competence_label"] = df_main["code_competence"]
            df_main["niveau_code"] = df_main["competence_label"] + "-N" + df_main["niveau"].astype(str)
            df_main["id_module"] = pd.to_numeric(df_main["id_module"], errors="coerce").fillna(0)
            df_main["id_semestre"] = pd.to_numeric(df_main["id_semestre"], errors="coerce")

            module_names = {"0": "Non associé"}

            for _, row in df_modules.iterrows():
                mid = row["id_module"]
                code = row.get("code_module") if pd.notna(row.get("code_module", float("nan"))) else f"M{mid}"
                nom = row.get("nom") if pd.notna(row.get("nom", float("nan"))) else "Module"
                module_names[str(int(float(mid)))] = f"{code} - {nom}"

            return {
                "df_main": df_main.to_json(date_format="iso", orient="split"),
                "df_modules": df_modules.to_json(date_format="iso", orient="split"),
                "df_composantes": df_composantes.to_json(date_format="iso", orient="split"),
                "module_names": module_names,
            }

        except Exception as e:
            logging.exception(f"[apc20_ens_data_loader] erreur chargement : {e}")
            return None