# learnagement
Learnagement (Learning management) est un outil d'intégration de données de l'enseignement, il a pour but de faire le pont entre étudiants, enseignants et administratifs. Il est principalement développé par les étudiants de l'USMB, ceux de la filière IDU de Polytech Annecy dans le cadre d'un apprentissage par projet et ceux de Licence de l'UFR SCEM dans le cadre de projets. 

L'App Web s'organise autour de différents objectifs enrichis par les axes de développement choisi par les étudiants et enseignants : la gestion du planning prévisionnel des enseignants, la cohérence entre le MCCC, le prévisionnel et la planification réelle, et la gestion des absences des étudiants...

## Prérequis
OS Unix ou Windows
Docker desktop
Python 3

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
python learnagement.py -start
```

Au 1e lancement, l'app vous demande le numéro d'instance 'I' compris entre 1 et 4. Trois services seront accessibles :  
- L'app web : 127.0.0.1:```i```0080;
- PhPMyAdmin : 127.0.0.1:```i```8080; root/<mot de passe défini à l'installation>

en remplaçant ```i``` par votre numéro d'instance.

## Utilisation

Lors du 1e lancement il vous sera demandé si vous souhaitez charger des données. 
Si vous avez chargé le jeu de données libres "small", vous trouverez via PhPMyAdmin un ensemble d'utilisateurs de test dont :
- un enseignant : FABRICE.LE_SAINT@truc.com / toto
- un étudiant : LAURENT.BONNIFAIT@machin.com / toto
- un administratif : pierre.tartampion@truc.com / toto

Pour tous les utilisateurs - administratif, enseignant ou étudiant - qui ont un mot de passe, ce dernier est ```toto```.

Si vous n'avez pas chargé de données de test, vous devrez saisir ou importer vos propres données

**Multi-instances** : 

Si vous souhaitez lancer plusieurs instances de Learnagement sur la même machine :
- Re-cloner le dépot GIT
- Re-faire la procédure de lancement initiale en changeant le nom et le numéro d'instance

Actuellement 3 instances en parallèle sont possibles.

## Arrêt de l'app

L'app s'arrête, sans perte de donnée, via la commande :  
```bash
python learnagement.py -stop
```

## Stop or Clean up from scratch the app


To destroy, remove all data to restart from scratch:  
```bash
python Learnagement -stop
python Learnagement -fromScratch
```

[Doc](Doc/doc.md) - [ToDo Lists](./ToDo/ToDo.md) - [CRediT](./CREDITS.md)
