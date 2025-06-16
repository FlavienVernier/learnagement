import mysql
import pandas as pd
import requests
import io

def get_students_without_stage():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = 'http://learnagement_phpbackend_dev/list/listEnseignant.php'
    resp = requests.post(url, data={}, headers=headers)
    urlData = resp.content
    return pd.read_json(io.StringIO(urlData.decode('utf-8')))