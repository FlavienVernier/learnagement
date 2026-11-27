# learnagement
Learnagement (Learning management) est un outil d'intégration de données de l'enseignement.
Il a pour but fonctionnel de faire le pont entre étudiants, enseignants et administratifs. 
Il est principalement développé par les étudiants de l'USMB, ceux de la filière IDU de Polytech Annecy dans le cadre d'un apprentissage par projet et ceux de Licence de l'UFR SCEM dans le cadre de projets. 

L'App Web s'organise autour de différents objectifs enrichis par les axes de développement choisi par les étudiants, enseignants et services administratifs : la gestion du planning prévisionnel des enseignants, la cohérence entre le MCCC, le prévisionnel et la planification réelle, la gestion des absences des étudiants...

## Architecture

Le diagramme ci-dessous présente la configuration Docker Compose de façon statique. Il ne prouve pas le démarrage ni les communications réelles des services. [ARCHITECTURE.md](ARCHITECTURE.md) est la référence complète.

<!-- mermaid-checked: no \n, no em-dash/en-dash, no {} in labels, subgraphs are id["label"], arrows are -->|"label"|, all subgraphs closed by end, ids unique -->
```mermaid
flowchart LR
    U["Navigateur"]
    CAS["CAS externe"]

    subgraph SERVICES["Services Compose sélectionnés pour l'instance"]
        MYSQL["data_mysql_INSTANCE"]
        PMA["phpmyadmin_INSTANCE"]
        API["backend_python_INSTANCE"]
        PHP["front_php_INSTANCE"]
        NEXT["front_nextjs_INSTANCE"]
        DASH["front_dashplotly_INSTANCE"]
        DB[("Compose volume learnagement_persistent_db_INSTANCE")]
    end

    FRONTNET["Réseau bridge learnagement_front_INSTANCE"]
    BACKNET["Réseau bridge learnagement_back_INSTANCE"]
    SOCKETNET["Socket network key learnagement_socket_proxy_INSTANCE"]

    subgraph OPTIONAL["Proxy optionnel si Traefik est sélectionné"]
        SOCKET["socket_proxy_INSTANCE"]
        TRAEFIK["reverse_proxy_traefik_INSTANCE"]
    end

    PHP -.->|"member"| FRONTNET
    NEXT -.->|"member"| FRONTNET
    DASH -.->|"member"| FRONTNET
    API -.->|"member"| FRONTNET
    API -.->|"member"| BACKNET
    MYSQL -.->|"member"| BACKNET
    PMA -.->|"member"| BACKNET
    TRAEFIK -.->|"member"| FRONTNET
    TRAEFIK -.->|"member"| BACKNET
    TRAEFIK -.->|"member"| SOCKETNET
    SOCKET -.->|"member"| SOCKETNET

    MYSQL -->|"stores data"| DB
    MYSQL -.->|"health gate: service_healthy"| API
    MYSQL -.->|"health gate: service_healthy"| PMA
    API -.->|"health gate: service_healthy"| PHP
    API -.->|"health gate: service_healthy"| NEXT
    API -.->|"health gate: service_healthy"| DASH
    SOCKET -.->|"service_healthy prerequisite"| TRAEFIK
    TRAEFIK -.->|"health gate when selected"| PHP
    TRAEFIK -.->|"health gate when selected"| PMA

    U -->|"published port when no proxy"| PHP
    U -->|"published port when proxy is off"| NEXT
    U -->|"published port when proxy is off"| DASH
    U -->|"loopback port when no proxy"| PMA
    U -->|"HTTPS route when proxy selected"| TRAEFIK
    TRAEFIK -->|"HTTPS route"| PHP
    TRAEFIK -->|"HTTPS route"| DASH
    TRAEFIK -->|"HTTPS route with BasicAuth"| PMA

    PHP -->|"HTTP dev; HTTPS configured prod"| API
    DASH -->|"HTTP dev; HTTPS configured prod"| API
    NEXT -->|"configured scheme; TLS trust unverified"| API
    API -->|"MySQL TCP 3306; TLS not enforced"| MYSQL
    PMA -->|"MySQL protocol; TLS not configured here"| MYSQL
    U -.->|"CAS login if configured"| CAS
    PHP -.->|"CAS_HOST serviceValidate; scheme is configurable"| CAS
```

MySQL utilise TCP 3306 uniquement sur le réseau Back; Compose ne publie pas ce port sur l'hôte. Les flèches de dépendance de santé partent du service requis vers le service dépendant. Le réseau socket proxy et le volume MySQL utilisent des clés Compose; Docker applique le nom du projet lorsqu'aucun nom explicite n'est défini.

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
