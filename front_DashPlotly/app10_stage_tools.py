import logging

from dotenv import load_dotenv
import os
import pandas as pd
import requests
import io

import app_tools

load_dotenv()

def get_stages_by_supervisorId(token, supervisorId):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/enseignants/{supervisorId}/stages"),
        token = token)
    return df

def get_stages_by_studentId(token, studentId):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url(f"/etudiants/{studentId}/stages"),
        token = token)
    return df


def get_stages_with_supervisorId(token):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("/etudiants/stages"),
        token = token)
    df = df.dropna()
    #df = df[df.notnull().any(axis=1)]
    return df

def get_stages_without_supervisorId(token):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("/etudiants/stages"),
        token=token)
    df = df[df.isnull().any(axis=1)]
    return df

def get_students_without_stage(token):
    df = app_tools.get_endpoint(
        url = app_tools.get_python_backend_url("/etudiants/without_stage"),
        token = token)
    return df

def add_stage(token, entreprise, sujet, mission, ville, start_date, end_date, id_etudiant, id_enseignant):
    try:
        df = app_tools.post_endpoint(
            url = app_tools.get_python_backend_url(f"/etudiants/{id_etudiant}/stage"),
            data={  'entreprise':entreprise,
                    'intitule':sujet,
                    'description':mission,
                    'ville':ville,
                    'date_debut':start_date,
                    'date_fin':end_date,
                    'nature':"",
                    'id_etudiant': id_etudiant,
                    'id_enseignant':id_enseignant},
            token = token)
        return "Data saved successfully"
    except Exception as e:
        logging.exception(e)

def set_internship_supervisor(token, id_etudiant, id_stage, new_supervisor_id):
    df = app_tools.patch_endpoint(
        url = app_tools.get_python_backend_url(f"/etudiants/{id_etudiant}/stages/{id_stage}"),
        data={'id_enseignant':new_supervisor_id},
        token = token)
    return df

def remove_stage(token, id_etudiant, id_stage):
    df = app_tools.delete_endpoint(
        url = app_tools.get_python_backend_url(f"/etudiants/{id_etudiant}/stages/{id_stage}"),
        token = token)
    return df