#!/bin/bash
set -e

echo "🚀 PHP container starting..."

cd /var/www/html

# Install dependencies only once
if [ -f composer.json ] ; then
    echo "📦 Installing Composer dependencies..."
    composer install --no-interaction
else
    echo "✅ Composer dependencies already installed."
fi

echo "🌐 Starting Apache..."
exec apache2-foreground