# Purpose: build the non-root PHP/Apache image on the Kubernetes service port.
FROM php:8.5-apache AS php-base

RUN apt-get update \
    && apt-get install -y --no-install-recommends libcurl4 libxml2 libcurl4-openssl-dev libxml2-dev \
    && docker-php-ext-install curl dom mysqli simplexml \
    && apt-get purge -y --auto-remove libcurl4-openssl-dev libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

FROM php-base AS dependencies

RUN apt-get update \
    && apt-get install -y --no-install-recommends unzip \
    && rm -rf /var/lib/apt/lists/*

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
WORKDIR /build
COPY front_PHP/composer.json front_PHP/composer.lock ./
RUN composer install \
    --no-dev \
    --no-interaction \
    --no-progress \
    --prefer-dist \
    --no-scripts \
    --no-plugins \
    --classmap-authoritative

FROM php-base

RUN a2enmod rewrite \
    && sed -i 's/^Listen 80$/Listen 8080/' /etc/apache2/ports.conf \
    && mkdir -p /var/run/apache2 /var/lock/apache2 \
    && chown -R www-data:www-data /var/run/apache2 /var/lock/apache2 /var/log/apache2

COPY docker/kubernetes/front-php/apache-kubernetes.conf /etc/apache2/sites-available/000-default.conf
COPY --chown=www-data:www-data front_PHP/ /var/www/html/
COPY --from=dependencies --chown=www-data:www-data /build/vendor/ /var/www/html/vendor/

WORKDIR /var/www/html
USER www-data:www-data
EXPOSE 8080
STOPSIGNAL SIGWINCH

CMD ["apache2-foreground"]
