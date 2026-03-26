#!/bin/sh

set -e

echo "🚀 PHP container starting..."

cd /var/www/html

# Install dependencies only once
if [ -f composer.json ] ; then
    echo "📦 Installing Composer dependencies..."
    composer update
    composer install --no-interaction
else
    echo "✅ Composer dependencies already installed. Just update"
fi

echo "🌐 Starting Apache..."
exec apache2-foreground