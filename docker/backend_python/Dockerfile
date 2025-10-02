# Utiliser l'image officielle de Node.js
FROM python:3

RUN mkdir /app
WORKDIR /app/

# Copier tout le code de l'application dans l'image
COPY startup.sh /
RUN chmod +x /startup.sh


# Exposer le port 3000 pour le serveur Next.js
EXPOSE 80

# Commande par défaut pour Docker Compose
CMD ["/bin/sh","-c","/startup.sh"]