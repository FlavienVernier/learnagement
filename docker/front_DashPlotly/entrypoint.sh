#!/bin/sh
# Be careful don't use bash and bash command

apt-get update && apt-get install -y graphviz && rm -rf /var/lib/apt/lists/*

cd /app

python -m venv docker_venv

. docker_venv/bin/activate

# Vérifier si l'installation a déjà été effectuée
if [ ! -f "docker_venv/.installed" ] || [ "requirements.txt" -nt "docker_venv/.installed" ]; then
    echo "Première installation des dépendances, ou nouvelle dépendance..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch docker_venv/.installed
else
    echo "Dépendances déjà installées, on passe..."
fi

python main.py