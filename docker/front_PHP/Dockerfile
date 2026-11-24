#FROM php:8-apache
#
#RUN apt-get update && apt-get upgrade -y
#RUN apt-get install sudo unzip wget -y
#RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli
#
#COPY --from=composer/composer:latest-bin /composer /usr/bin/composer
#
#WORKDIR /var/www/html
#
#RUN a2enmod rewrite
#RUN a2enmod ssl
#
#COPY apache.conf /etc/apache2/sites-available/000-default.conf
#
## Working directory
#WORKDIR /var/www/html
#
## Copie les vhosts
#COPY ssl.conf /etc/apache2/sites-available/ssl.conf
##COPY default.conf /etc/apache2/sites-available/000-default.conf
#
## Activer le site SSL
## RUN a2ensite ssl.conf
#
## Copy entrypoint
#COPY entrypoint.sh /entrypoint.sh
#RUN chmod +x /entrypoint.sh \
#    && sed -i 's/\r$//' /entrypoint.sh
#
#EXPOSE 80
#EXPOSE 443
#
## IMPORTANT: use entrypoint, not command
#ENTRYPOINT ["/entrypoint.sh"]

############## base : OS ##############
FROM php:8.5-apache AS base
# TODO : épingler (version mineure que tu utilises vraiment, idéalement par digest)

RUN apt-get update \
 && apt-get install -y --no-install-recommends unzip \
 && rm -rf /var/lib/apt/lists/*
RUN docker-php-ext-install mysqli          # l'extension est activée automatiquement

COPY --from=composer/composer:2-bin /composer /usr/bin/composer

RUN a2enmod rewrite ssl
COPY apache.conf /etc/apache2/sites-available/000-default.conf
COPY ssl.conf    /etc/apache2/sites-available/ssl.conf

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh \
 && chmod 755 /usr/local/bin/entrypoint.sh

WORKDIR /var/www/html
EXPOSE 80 443
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

############## dev : code monté en volume ##############
FROM base AS dev
ENV ENV=dev

############## prod : code et dépendances dans l'image ##############
FROM base AS prod
ENV ENV=prod
RUN a2ensite ssl.conf
COPY --from=os . /var/www/html
RUN if [ -f composer.json ]; then \
        composer install --no-dev --optimize-autoloader --no-interaction; \
    fi