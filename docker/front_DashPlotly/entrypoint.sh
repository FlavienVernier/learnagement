#!/bin/sh
# Be careful don't use bash and bash command

cd /app

VENV_PATH=/opt/docker_venv
python -m venv "$VENV_PATH"

. "$VENV_PATH/bin/activate"

# Réinstaller si les dépendances ont changé depuis la dernière installation.
requirements_hash=$(sha256sum requirements.txt | cut -d ' ' -f 1)
installed_hash=""
if [ -f "$VENV_PATH/.installed" ]; then
    installed_hash=$(cat "$VENV_PATH/.installed")
fi

if [ "$installed_hash" != "$requirements_hash" ]; then
    echo "Première installation des dépendances..."
    pip install --upgrade pip
    pip install -r requirements.txt
    printf '%s' "$requirements_hash" > "$VENV_PATH/.installed"
else
    echo "Dépendances déjà installées, on passe..."
fi

python main.py