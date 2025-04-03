# learnagement
Learnagement (Learning management) est un outil d'intégration de données de l'enseignement, il a pour but de faire le pont entre étudiants, enseignants et administratifs. Il est principalement développé par les étudiants de l'USMB, ceux de la filière IDU de Polytech Annecy dans le cadre d'un apprentissage par projet et ceux de Licence de l'UFR SCEM dans le cadre de projets. 

L'App Web s'organise autour de différents objectifs enrichis par les axes de développement choisi par les étudiants et enseignants : la gestion du planing prévisionel des enseignants, la cohérence entre le MCCC le prévisionel et la planification réelle, et la gestion des abscences des étudiants...

## Pré-requis
OS Unix ou windows
Docker et docker-compose
Python 3

## Installation et lancement

L'app se lance (LAMP) sous docker
"learnagement.py"

## Arrêt de l'app

L'app s'arrête, sans perte de donnée, vie la commande:
learnagement.py -stop

## Stop or Clean up (destroy) the app

To stop:
python Learnagement -stop

To destroy, remove all data to restart from scratch, the app must be stoped:
python Learnagement -destroy

[ToDo Lists](./ToDo/ToDo.md) - [Norm](./Norm/Norm.md) - [CRediT](./CREDITS.md)
