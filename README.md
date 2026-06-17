# learnagement
Learnagement (Learning management) est un outil d'intégration de données de l'enseignement.
Il a pour but fonctionnel de faire le pont entre étudiants, enseignants et administratifs. 
Il est principalement développé par les étudiants de l'USMB, ceux de la filière IDU de Polytech Annecy dans le cadre d'un apprentissage par projet et ceux de Licence de l'UFR SCEM dans le cadre de projets. 

L'App Web s'organise autour de différents objectifs enrichis par les axes de développement choisi par les étudiants, enseignants et services administratifs : la gestion du planning prévisionnel des enseignants, la cohérence entre le MCCC, le prévisionnel et la planification réelle, la gestion des absences des étudiants...



## Prérequis
OS X, Unix or Windows,
Docker desktop,
Python 3.

## Installation et lancement

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
