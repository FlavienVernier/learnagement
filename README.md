# learnagement
Learnagement (Learning management) est un outil d'intégration de données de l'enseignement, il a pour but de faire le pont entre étudiants, enseignants et administratifs. Il est principalement développé par les étudiants de l'USMB, ceux de la filière IDU de Polytech Annecy dans le cadre d'un apprentissage par projet et ceux de Licence de l'UFR SCEM dans le cadre de projets. 

L'App Web s'organise autour de différents objectifs enrichis par les axes de développement choisi par les étudiants et enseignants : la gestion du planning prévisionnel des enseignants, la cohérence entre le MCCC, le prévisionnel et la planification réelle, et la gestion des absences des étudiants...

## Prérequis
OS Unix ou Windows
Docker et docker-compose
Python 3

## Installation et lancement

L'app se lance (LAMP) sous docker:  
```bash
python learnagement.py
```

Au 1e lancement, l'app vous demande le numéro d'instance 'I' compris entre 1 et 4. Trois services seront accessibles :  
- L'app web : 127.0.0.1:I0080;
- PhPMyAdmin : 127.0.0.1:I8080;

en remplaçant 'I' par votre numéro d'instance.

## Arrêt de l'app

L'app s'arrête, sans perte de donnée, via la commande:  
```bash
python learnagement.py -stop
```

## Stop or Clean up (destroy) the app

To stop:  
```bash
python Learnagement -stop
```

To destroy, remove all data to restart from scratch, the app must be stopped:  
```bash
python Learnagement -destroy
```

[Tuto](./TUTO.md) - [ToDo Lists](./ToDo/ToDo.md) - [Norm](./Norm/Norm.md) - [CRediT](./CREDITS.md)
