from app_tools import get_endpoint, get_python_backend_url


def get_apc_competences(token):
    url = get_python_backend_url("apc/competences/")
    return get_endpoint(url, token=token)


def get_apc_niveaux(token):
    url = get_python_backend_url("apc/niveaux/")
    return get_endpoint(url, token=token)


def get_apc_apprentissages(token):
    url = get_python_backend_url("apc/apprentissages/")
    return get_endpoint(url, token=token)


def get_apc_ac_modules(token):
    url = get_python_backend_url("apc/ac_modules/")
    return get_endpoint(url, token=token)


def get_apc_modules(token):
    url = get_python_backend_url("apc/modules/")
    return get_endpoint(url, token=token)


def get_apc_composantes(token):
    url = get_python_backend_url("apc/composantes/")
    return get_endpoint(url, token=token)


def get_apc_situations(token):
    url = get_python_backend_url("apc/situations/")
    return get_endpoint(url, token=token)
