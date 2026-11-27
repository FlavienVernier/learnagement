# learnagement
Learnagement (Learning management) est un outil d'intégration de données de l'enseignement.
Il a pour but fonctionnel de faire le pont entre étudiants, enseignants et administratifs. 
Il est principalement développé par les étudiants de l'USMB, ceux de la filière IDU de Polytech Annecy dans le cadre d'un apprentissage par projet et ceux de Licence de l'UFR SCEM dans le cadre de projets. 

L'App Web s'organise autour de différents objectifs enrichis par les axes de développement choisi par les étudiants, enseignants et services administratifs : la gestion du planning prévisionnel des enseignants, la cohérence entre le MCCC, le prévisionnel et la planification réelle, la gestion des absences des étudiants...

## Architecture

Cette vue résume la topologie Docker Compose : PHP, Next.js, Dash, Backend, MySQL et phpMyAdmin, les réseaux Front/Back et les flux confirmés. Elle distingue les composants optionnels et les services externes; elle ne constitue pas une preuve de fonctionnement runtime. [ARCHITECTURE.md](ARCHITECTURE.md) est la référence complète.

```mermaid
flowchart LR
    Browser["Navigateur"]

    subgraph Interfaces["Interfaces utilisateur"]
        PHP["PHP"]
        Next["Next.js"]
        Dash["Dash"]
    end

    Backend["Backend Python"]
    MySQL[("MySQL")]
    PMA["phpMyAdmin"]
    Volume[("Volume MySQL Docker")]

    FrontNet["Réseau Front Docker"]
    BackNet["Réseau Back Docker"]
    SocketNet["Réseau socket proxy"]

    subgraph ProxyOptionnel["Proxy optionnel"]
        Traefik["Traefik"]
        SocketProxy["Socket proxy Docker"]
    end

    CAS["CAS externe"]
    Groq["API Groq"]

    PHP -.->|"membre du réseau"| FrontNet
    Next -.->|"membre du réseau"| FrontNet
    Dash -.->|"membre du réseau"| FrontNet
    Backend -.->|"membre du réseau"| FrontNet
    Backend -.->|"membre du réseau"| BackNet
    MySQL -.->|"membre du réseau"| BackNet
    PMA -.->|"membre du réseau"| BackNet
    Traefik -.->|"membre du réseau"| FrontNet
    Traefik -.->|"membre du réseau"| BackNet
    Traefik -.->|"membre du réseau"| SocketNet
    SocketProxy -.->|"membre du réseau"| SocketNet

    Browser -->|"port direct sans proxy"| PHP
    Browser -->|"port direct sans proxy"| Next
    Browser -->|"port direct sans proxy"| Dash
    Browser -->|"port local ou route protégée"| PMA
    Browser -->|"HTTPS si configuré"| Traefik
    Traefik -->|"route HTTPS"| PHP
    Traefik -->|"route HTTPS"| Dash
    Traefik -->|"route HTTPS avec BasicAuth"| PMA

    PHP -->|"HTTP ou HTTPS configuré"| Backend
    Next -->|"HTTP ou HTTPS configuré"| Backend
    Dash -->|"HTTP ou HTTPS configuré"| Backend
    Backend -->|"TCP 3306"| MySQL
    PMA -->|"administration SQL"| MySQL
    MySQL -->|"données persistantes"| Volume
    PHP -->|"validation de ticket"| CAS
    Dash -->|"requêtes chatbot"| Groq

    MySQL -.->|"service healthy requis"| Backend
    MySQL -.->|"service healthy requis"| PMA
    Backend -.->|"service healthy requis"| PHP
    Backend -.->|"service healthy requis"| Next
    Backend -.->|"service healthy requis"| Dash
    SocketProxy -.->|"service healthy requis"| Traefik
    Traefik -.->|"service healthy requis"| PHP
    Traefik -.->|"service healthy requis"| PMA

    classDef ui fill:#DBEAFE,stroke:#1D4ED8,color:#1E3A8A,stroke-width:2px;
    classDef backend fill:#DCFCE7,stroke:#15803D,color:#14532D,stroke-width:2px;
    classDef data fill:#FEF3C7,stroke:#B45309,color:#78350F,stroke-width:2px;
    classDef network fill:#E5E7EB,stroke:#4B5563,color:#111827,stroke-width:2px;
    classDef optional fill:#F3E8FF,stroke:#7E22CE,color:#581C87,stroke-width:2px;
    classDef external fill:#FCE7F3,stroke:#BE185D,color:#831843,stroke-width:2px;

    class Browser,PHP,Next,Dash ui;
    class Backend backend;
    class MySQL,Volume data;
    class FrontNet,BackNet,SocketNet network;
    class PMA,Traefik,SocketProxy optional;
    class CAS,Groq external;
```

**Légende :** bleu = interfaces; vert = Backend; ambre = MySQL et persistance; gris = réseaux; violet = composants optionnels; rose = intégrations externes. Les traits pleins représentent les appels et les données; les pointillés représentent l'appartenance réseau ou une dépendance de santé Compose.

Le Backend est connecté aux deux réseaux; MySQL et phpMyAdmin sont sur Back. Le port MySQL n'est pas publié sur l'hôte. Groq est appelé directement par le chatbot Dash; aucun service IA autonome ni Ollama n'est représenté comme composant Learnagement confirmé.

Pour les ressources Kubernetes préliminaires et leurs limites, consulter [la documentation de la base](kubernetes/base/README.md) et [la checklist de déploiement](docs/kubernetes-deployment-checklist.md). Les manifests n'ont pas été appliqués à un cluster.

## Prérequis
OS X, Unix or Windows,
Docker desktop,
Python 3.

## Installation et lancement

### Dev Mode (Bootstrap)

Création de l'environnement, installation ou mise à jour des requirements, lancement de l'app
```bash
python3 bootstrap.py
```
L'environnement sera créé dans /.venv

### Dev Mode (a la mano)

Initialisation de l'environnement à ne faire qu'une seule fois
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```


L'app se lance avec docker (pensez à lancer docker-desktop):
```bash
source ./venv/bin/activate
python Learnagement.py start
```

To configure your instance, edit specific ".env_XXX.env" files and restarts the app with:
```bash
python Learnagement.py start --env XXX
```

For any help
```bash
python Learnagement.py --help
```

### Production Mode

Generate self certificate:
```bash
python Learnagement_Security.py 
```

Generate environment
```bash
python bootstrap.py generate-env --env prod
```

Edit the .env file to configure your instance.

Run with prod environnement (secure):
```bash
source .venv/bin/activate
python Learnagement.py start --env prod
```
Note, containers will rebuild.


## Utilisation

Lors du 1e lancement il vous sera demandé si vous souhaitez charger des données. 
Si vous avez chargé le jeu de données libres "small", vous trouverez via PhPMyAdmin un ensemble d'utilisateurs de test dont :
- un enseignant : AMELIE.CODRON@truc.com / toto
- un étudiant : LAURENT.BONNIFAIT@machin.com / toto
- un administratif : pierre.tartampion@truc.com / toto

Pour tous les utilisateurs - administratif, enseignant ou étudiant - qui ont un mot de passe, ce dernier est ```toto```.

Si vous n'avez pas chargé de données de test, vous devrez saisir ou importer vos propres données

**Multi-instances** : 

Si vous souhaitez lancer plusieurs instances de Learnagement sur la même machine :
- Re-cloner le dépot GIT
- Re-faire la procédure de lancement initiale en changeant le nom et le numéro d'instance

Actuellement 4 instances en parallèle sont possibles.

## Arrêt de l'app

L'app s'arrête, sans perte de donnée, via la commande :  
```bash
python Learnagement.py -stop
```

## Stop or Clean up from scratch the app


To destroy, remove all data to restart from scratch:  
```bash
python Learnagement.py stop
python Learnagement.py start --from_scratch
```

## Major upgrade

- step 1: back-up your DB
```bash 
python Learnagement.py backupdb
```
- step 3: stop the current instance
```bash
python Learnagement.py stop
```
- step 4: deactivate your python environment
- step 4: move out of your Learnagement directory, get a new clone of Learnagement git, create, activate a new python environment and install requirements 
- step 5: move into the new repository and switch to the required branch
- step 6: create "./db/data/" directory and copy your backed-up data into
```bash 
mkdir ./db/data/
cp /[INITIAL PATH TO LEARNAGEMENT]/db/backup/VX.X.X__data_XXX[CURENT DATE].sql ./db/data/
```
- step 7: start the new instance (it will start like 1st time, so given the same port to the old instance to keep the service continuity)
```bash
python Learnagement.py start
```

[Doc](Doc/doc.md) - [ToDo Lists](./ToDo/ToDo.md) - [CRediT](./CREDITS.md) - [Licence](./LICENSE)
