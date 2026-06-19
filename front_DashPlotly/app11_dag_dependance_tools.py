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

def add_dependance_to_idModule(token, id_module:int, id_sequence_prev:int, id_sequence_next:int):
    try:
        df = app_tools.post_endpoint(
            url = app_tools.get_python_backend_url(f"/modules/{id_module}/dependencies/"),
            data={  'id_sequence_prev': id_sequence_prev,
                    'id_sequence_next': id_sequence_next},
            token=token)
        return f"Module {id_module} link from {id_sequence_prev} to {id_sequence_next} added"
    except Exception as e:
        logging.exception(e)
        return str(e)

def delete_dependencie_to_idModule(token, id_module:int, id_sequence_prev:int, id_sequence_next:int):
    try:
        df = app_tools.delete_endpoint(
            url = app_tools.get_python_backend_url(f"/modules/{id_module}/dependencies/{id_sequence_prev}/{id_sequence_next}"),
            token=token
        )
        return f"Module {id_module} link from {id_sequence_prev} to {id_sequence_next} deleted"
    except Exception as e:
        logging.exception(e)
        return str(e)
