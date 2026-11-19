#!/bin/sh

set -e

echo "PHP container starting..."

cd /var/www/html

# Installer les dépendances seulement si vendor/ est absent
if [ -f composer.json ]; then
    if [ ! -f vendor/autoload.php ]; then
        echo "Installing Composer dependencies..."
        composer install --no-interaction --no-progress || \
            echo "WARNING: composer install a échoué (réseau ?), démarrage sans dépendances"
    else
        echo "Composer dependencies already installed."
    fi
fi

# Activer le vhost SSL uniquement en production
if [ -f .env ]; then
    INSTANCE_NAME=$(grep -E '^INSTANCE_NAME=' .env | cut -d '=' -f2 | tr -d '\r')
fi

if [ "$ENV" = "prod" ]; then
    echo "Production détectée — activation du vhost SSL..."
    a2enmod ssl
    a2ensite ssl.conf
else
    echo "Environnement non-prod ($INSTANCE_NAME) — SSL vhost ignoré."
fi

echo "Starting Apache..."
exec apache2-foreground