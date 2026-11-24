#!/bin/sh
# Be careful don't use bash and bash command
set -eu
cd /app

# Dépendances : seulement en dev (en prod elles sont dans l'image)
if [ "$ENV" != "prod" ]; then
    STAMP=/opt/venv/.installed
    if [ ! -f "$STAMP" ] || [ requirements.txt -nt "$STAMP" ] || [ requirements-dev.txt -nt "$STAMP" ]; then
        echo "Installation des dépendances..."
        pip install --upgrade pip
        pip install -r requirements.txt -r requirements-dev.txt
        touch "$STAMP"
    else
        echo "Dépendances déjà installées, on passe..."
    fi

    # -p no:cacheprovider : pas d'écriture de .pytest_cache (code monté en :ro)
    pytest -p no:cacheprovider || echo "Tests échoués"
fi

# exec : python devient PID 1 et reçoit SIGTERM (arrêt propre du conteneur)
exec python main.py