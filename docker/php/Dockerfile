FROM php:8-apache

RUN apt-get update && apt-get upgrade -y
RUN apt-get install sudo unzip wget -y
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

COPY --from=composer/composer:latest-bin /composer /usr/bin/composer

WORKDIR /var/www/html

RUN a2enmod rewrite
RUN a2enmod ssl

COPY apache.conf /etc/apache2/sites-available/000-default.conf

# Working directory
WORKDIR /var/www/html

# Copie les vhosts
COPY ssl.conf /etc/apache2/sites-available/ssl.conf
#COPY default.conf /etc/apache2/sites-available/000-default.conf

# Activer le site SSL
# RUN a2ensite ssl.conf

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && sed -i 's/\r$//' /entrypoint.sh

EXPOSE 80
EXPOSE 443

# IMPORTANT: use entrypoint, not command
ENTRYPOINT ["/entrypoint.sh"]

