import importlib
import pkgutil
import sys


def get_all_requests(package_name: str) -> dict:
    """
    Récupère la variable 'requests' de tous les modules d'un package.
    Retourne un dict {nom_module: requests}
    """
    package = importlib.import_module(package_name)
    results = {}
    for importer, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        full_name = f"{package_name}.{module_name}"
        module = importlib.import_module(full_name)

        if hasattr(module, "requests"):
            results[module_name] = module.requests

    return results


def get_all_local_requests() -> dict:
    # Récupère le package parent (le dossier contenant access_auth.py)
    package_name = __name__.rsplit(".", 1)[0]
    package = sys.modules[package_name]

    results = {}

    for importer, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        full_name = f"{package_name}.{module_name}"
        module = importlib.import_module(full_name)

        if hasattr(module, "requests"):
            results[module_name] = module.requests

    return results
