# Utiliser l'image officielle de Node.js
FROM node:18-alpine

# Définir le répertoire de travail dans le conteneur
RUN mkdir /app
WORKDIR /app

# Copier les fichiers nécessaires pour installer les dépendances
#COPY package.json package-lock.json ./

# Supprimer les dépendances existantes et les réinstaller
#RUN npm install

# Copier tout le code de l'application dans l'image
COPY startup.sh /
RUN chmod +x /startup.sh

# Exposer le port 3000 pour le serveur Next.js
EXPOSE 5173

# Commande par défaut pour Docker Compose
#CMD ["/bin/sh","-c","ls", "-l", "./startup.sh"]
#CMD npm install & npm run dev	
CMD ["/bin/sh","-c","/startup.sh"]
#CMD ["npm", "run", "dev"]