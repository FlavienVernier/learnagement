# Utiliser l'image officielle de Node.js
FROM python:3

RUN mkdir /app
WORKDIR /app/

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && sed -i 's/\r$//' /entrypoint.sh


# Exposer le port 3000 pour le serveur Next.js
EXPOSE 80

# IMPORTANT: use entrypoint, not command
ENTRYPOINT ["/entrypoint.sh"]