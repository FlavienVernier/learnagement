#!/bin/sh
# Be careful don't use bash and bash command

cd /app

python -m venv docker_venv

. docker_venv/bin/activate

# Vérifier si l'installation a déjà été effectuée
if [ ! -f "docker_venv/.installed" ]; then
    echo "Première installation des dépendances..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch docker_venv/.installed
else
    echo "Dépendances déjà installées, on passe..."
fi

python main.py