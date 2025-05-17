# DOC_TECHNIQUE

# Documentation Technique - Learnagement

## Architecture du Projet

### Vue d’ensemble

1. **Backend (webApp)**
    - Architecture PHP traditionnelle
    - Gestion des données via des fichiers PHP
    - Système de CRUD (Create, Read, Update, Delete)
2. **Frontend (webappnext**
    - Framework Next.js
    - Styling avec Tailwind CSS
    - Typage avec TypeScript

### Architecture Backend

### Structure des Dossiers

```
webApp/
├── connection/       # Gestion des connexions
├── crud/             # Opérations CRUD
├── db_connection/    # Connexions à la base de données
├── list/             # Requêtes retournant une liste de données
└── select/           # Requêtes retournant une seule donnée
```

### Architecture Frontend

### Structure des Dossiers

```
webappnext/
├── app/               # Pages et composants Next.js
├── lib/               # Bibliothèques utilitaires
├── public/            # Assets statiques (icones, logos etc...)
├── .env               # variables d'environnements (pour NextAuth.js : NEXTAUTH_URL=http://localhost:40080/, NEXTAUTH_SECRET=[à générer cf. NextAuth.js doc]) 
└── tailwind.config.ts # Fichier de configuration tailwind
```

### Technologies Frontend

- **Next.js** : Framework React
- **Tailwind CSS** : Framework CSS
- **TypeScript** : Typage statique pour JavaScript

### Connexion

**Principe de la connexion**

Lors de la connexion, une requête est envoyée au back (PHP) afin de vérifier si les identifiants sont bons, s’ils le sont alors une session PHP est créée (voir fichier côté PHP : `connection/authenticate.php`), un cookie contenant le `PHPSESSID` est envoyé au front (Next.js).

Côté front la connexion est gérée par la librairie NextAuth.js. Elle permet de gérer la session des utilisateurs et, via un middleware (voir fichier `middleware.ts`), de protéger les pages qui sont accessibles uniquement après connexion. Le fichier qui gère la logique d’identification côté nextJs est `api/proxy/auth/[...nextauth]/route.ts`. C’est dans ce fichier qu’on fait une requête vers le PHP pour savoir si les identifiants sont bons. S’ils le sont, le `PHPSESSID` est reçu et stocké dans un cookie, pour être utilisé pour les futures requêtes vers le PHP.

![image.png](images/image.png)

Voici un schéma de la documentation officielle de NextAuth.js, qui montre comment l’authentification fonctionne.

**Utiliser la session côté client**

Pour vérifier si un utilisateur est connecté pour effectué une redirection, il suffit d’utiliser `useSession` 

Exemple de redirection si l’utilisateur est connecté :

```jsx
import {useSession} from "next-auth/react"

export default function example(){
	    const {data: session, status} = useSession()
	    
	    useEffect(() => {
        if (status == 'authenticated'){
            router.push('/homepage')
        }
    }, [session]);
}
```

### Communication Front/Back - **Système de Proxy interne**

1. **Structure**
    - Implémenté dans `/app/api/proxy/[...phpPath]/route.ts`
    - Gère les requêtes GET et POST
    - Redirige vers le backend PHP
2. **Fonctionnement**
    
    ```tsx
    // Exemple de requête depuis le frontend axios.get('/api/proxy/get_filieres')
    ```
    
    - Capture la requête
    - Récupère le chemin après `/api/proxy/`
    - Redirige vers le backend (`http://php/get_filieres.php`) php correspond au nom du service docker.
    - Transfère les headers et le corps
    - Retourne la réponse au frontend
3. **Gestion des Headers**
    - Transfert des headers Content-Type
    - Maintien des cookies via le header
    - Configuration withCredentials: true
4. **Gestion des Erreurs**
    - Capture des erreurs avec `.catch()`
    - Affichage des messages d’erreur
    - Gestion des états de chargement

### Gestion des Sessions

1. **Côté back**
    - Transmis via les headers
    - Maintient la session PHP
2. **Côté front**
    - NextAuth.js gère les sessions à travers `useSession`

### Ajout de Nouvelles Fonctionnalités

### Frontend

1. **Créer un Nouveau Composant**
    - Créer un nouveau fichier dans `/app`
    - Utiliser TypeScript pour le typage
    - Utiliser Tailwind CSS pour le styling
2. **Ajouter une Nouvelle Route**
    - Créer un nouveau dossier dans `/app`
    - Implémenter la logique de la page
    - Configurer la navigation
3. **Page accessible uniquement après la connexion**
    - Ajouter dans `middleware.ts` l’url relative de la page

### Ajout d’images pour les filières

- Nom de l’image : nom court en **minuscule** de la filière correspondante
- Formats acceptés : `svg` ou `png`.
- Taille : 64x64 px.
- Emplacement : `public/logos/monImage.svg`

### Backend

1. **Gérer une nouvelle table SQL**
    - Créer un nouveau fichier PHP dans `/crud`
    - Implémenter les fonctions CRUD
2. **Accéder au données de la nouvelle table**
    - Créer un nouveau fichier PHP dans le dossier correspondant ex: `select`, `list` etc…
    - Implémenter la logique de la requête
    - Renvoyer les données au format `JSON` avec le flag `JSON_NUMERIC_CHECK`

### Meilleures Pratiques

1. **Frontend**
    - Utiliser TypeScript pour le typage
    - Utiliser les composants réutilisables
    - Gérer les états de chargement
    - Respecter l’arborescence des dossiers et fichiers
    - Utiliser la libraire zod pour vérifier les inputs des formulaires
2. **Backend**
    - Utiliser les fonctions existantes
    - Gérer les erreurs
    - Maintenir la cohérence des données
    - Respecter l’arborescence des dossiers et fichiers
    - Si un fichier change de place il est nécessaire de répercuter la modification au niveau du front
