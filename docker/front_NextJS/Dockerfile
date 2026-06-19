# Utiliser l'image officielle de Node.js
FROM node:18-alpine

#RUN apk add --no-cache --upgrade bash

# Définir le répertoire de travail dans le conteneur
RUN mkdir /app
WORKDIR /app

# Copier les fichiers nécessaires pour installer les dépendances
#COPY package.json package-lock.json ./

# Supprimer les dépendances existantes et les réinstaller
#RUN npm install

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && sed -i 's/\r$//' /entrypoint.sh

# Exposer le port 3000 pour le serveur Next.js
EXPOSE 3000

# IMPORTANT: use entrypoint, not command
ENTRYPOINT ["/entrypoint.sh"]