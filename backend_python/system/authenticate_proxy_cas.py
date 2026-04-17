import os
import dotenv
from typing import Annotated


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import re

from dependencies import logger, get_user, Token
from system.authenticate_tools import create_access_token

dotenv.load_dotenv(".env")

CAS_PROXY_HOST = os.getenv("CAS_PROXY_HOST")
CAS_HOST = os.getenv("CAS_HOST")
CAS_PROXY_LOOK4 = os.getenv("CAS_PROXY_LOOK4")  # "uid" par défaut

# app = FastAPI()
#
def init_cas_proxy(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # À restreindre en production
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Stockage des sessions en mémoire (session_id → cookies)
sessions: dict[str, httpx.Cookies] = {}


def get_redirect_location(response: httpx.Response) -> str | None:
    return response.headers.get("location")


def get_csrf_token(html: str) -> str | None:
    match = re.search(r'<input[^>]+name="execution"[^>]+value="([^"]+)"', html)
    return match.group(1) if match else None

import xml.etree.ElementTree as ET

def parse_cas_attributes(xml_response: str) -> dict | None:
    """Parse la réponse XML du CAS et retourne les attributs utilisateur."""
    try:
        root = ET.fromstring(xml_response)
        ns   = {"cas": "http://www.yale.edu/tp/cas"} #universal name space for CAS XML

        # Échec d'authentification
        failure = root.find(".//cas:authenticationFailure", ns)
        if failure is not None:
            return None

        # Succès : récupère les attributs
        attrs = root.find(".//cas:attributes", ns)
        if attrs is None:
            return {}

        return {child.tag.split("}")[-1]: child.text for child in attrs}

    except ET.ParseError:
        return None


async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    cookies = httpx.Cookies()

    async with httpx.AsyncClient(cookies=cookies, follow_redirects=False, verify=True) as client:

        # --- Étape 1 : accès intranet → redirection CAS ---
        step1   = await client.get(CAS_PROXY_HOST)
        cas_url = get_redirect_location(step1)

        # Extraction de l'URL de service (pour la validation du ticket)
        match = re.search(r'service=([^&]+)', cas_url) if cas_url else None
        service_url = match.group(1) if match else None


        if not cas_url:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Pas de redirection CAS",
            )

        # --- Étape 2 : chargement du formulaire CAS ---
        step2     = await client.get(cas_url)
        execution = get_csrf_token(step2.text)

        if not execution:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail='Token CAS "execution" introuvable',
            )

        # --- Étape 3 : POST des identifiants ---
        step3 = await client.post(cas_url, data={
            "username":    form_data.username,
            "password":    form_data.password,
            "execution":   execution,
            "_eventId":    "submit",
            "geolocation": "",
        })

        # --- Étape 4 : suivi des redirections post-auth ---
        current      = step3
        ticket        = None
        max_redirects = 5

        while (location := get_redirect_location(current)) and max_redirects > 0:

            # Cherche le ticket ST- dans l'URL de redirection
            ticket_match = re.search(r'ticket=(ST-[^&]+)', location)
            if ticket_match:
                ticket = ticket_match.group(1)

        # --- Étape 5 : validation du ticket → attributs utilisateur ---
        user_attributes = {}
        if ticket and service_url:
            validate_url = f"{CAS_HOST}/serviceValidate?ticket={ticket}&service={service_url}"
            validation   = await client.get(validate_url)
            user_attributes = parse_cas_attributes(validation.text) or {}

            current       = await client.get(location)
            max_redirects -= 1

        # --- Échec d'authentification ---
    if not user_attributes:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user(form_data.username, method="byLogin")

    # --- Génération du token ---
    access_token = create_access_token(
        data={"id": user.id,
              "email": user.mail,
              "firstname": user.prenom,
              "lastname": user.nom,
              "roles" : user.roles,
              "password2update" : user.password2update
              },
    )

    logger.info(f"User {user_attributes.get('mail')} connected via CAS")
    return Token(access_token=access_token, token_type="bearer")

async def logout(session_id: str = Form(...)):
    sessions.pop(session_id, None)
    return JSONResponse({"status": "logged_out"})