FROM php:8-apache

RUN apt-get update && apt-get upgrade -y
RUN apt-get install sudo unzip wget -y
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

COPY --from=composer/composer:latest-bin /composer /usr/bin/composer

#WORKDIR /var/www/html
#COPY composer.json composer.json
#COPY composer.lock composer.lock
#RUN composer install \
#    --no-interaction \
#    --no-plugins \
#    --no-scripts \
#    --no-dev \
#    --prefer-dist

#RUN composer dump-autoload


RUN a2enmod rewrite
RUN a2enmod ssl

# Working directory
WORKDIR /var/www/html

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

# IMPORTANT: use entrypoint, not command
ENTRYPOINT ["/entrypoint.sh"]

