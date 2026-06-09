"""
Fonctions d'accès aux données APC pour le dashboard enseignant.
Miroir de apc20_heatmap_apc_tools.py — réexporte les mêmes helpers
pour éviter les imports croisés entre sous-modules.
"""
from .apc20_heatmap_apc_tools import (
    get_apc_competences,
    get_apc_niveaux,
    get_apc_apprentissages,
    get_apc_ac_modules,
    get_apc_modules,
    get_apc_composantes,
    get_apc_situations,
)

__all__ = [
    "get_apc_competences",
    "get_apc_niveaux",
    "get_apc_apprentissages",
    "get_apc_ac_modules",
    "get_apc_modules",
    "get_apc_composantes",
    "get_apc_situations",
]
