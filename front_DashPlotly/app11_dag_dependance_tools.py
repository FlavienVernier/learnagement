import logging
from dotenv import load_dotenv
import pandas as pd
import app_tools

load_dotenv()

def get_list_dependance_by_idModule(token, id_module:int):

    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{id_module}/dependencies/"),
        data={'id_module': id_module},
        token=token)
    return df


def get_list_sequence_dependance_by_idModule(token, id_module:int):

    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/modules/{id_module}/sequence_dependencies/"),
        data={'id_module': id_module},
        token=token)
    return df

