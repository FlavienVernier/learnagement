# Lancement en local via Docker sur Windows

Bienvenue sur ce tuto détaillé pour l'installation et le lancement de learnagement pour Windows.

## Pré-requis

- windows
- Docker et docker-compose
- Python 

## Installation

1. Dans le dossier visualisation/visu
confirgurer le fichier de log de la manière suivante :

    ```
    root
    <mot de passe admin>
    mysql_<nom de votre instance>
    3306
    learnagement
    ```

2. Démarrer l'application Docker Desktop
3. Executer la commande dans votre console:

    ```bash
    python learnagment.py
    ```
4. Pour que la base de donnée soit pré-remplie, il faut répondre _y_ à la question _Do you want free data?_ Sinon repondre _n_
5. Entrer un `<nom pour votre instance>`
6. Choisir un `<mot de passe admin>` 
7. Créer un `<mot de passe utilisateur>` 

Si l'installation est réussie, aller sur un navigateur web en `localhost` pour accéder au projet learnagement.

## Lancement 

 Après l'installation, réexécuter la commande pour relancer l'App:

 ```bash
python Learnagement.py
```

## Free Data

L'installation propose d'utiliser des données libres pour tester l'application, 3 utilisateurs par défaut sont créés :

- un enseignant : FABRICE.LE_SAINT@truc.com / toto
- un étudiant : LAURENT.BONNIFAIT@machin.com / toto
- un administratif : pierre.tartampion@truc.com / toto


## Faire une autre installation 

Pour créer une autre instance :

1. Cloner le git dans un nouveau répertoire 
2. Reprendre les étapes de l'[installation](#installation)

    > [!CAUTION] 
    > Les différentes installations doivent impérativement avoir des noms et des numéros d'instance différents !

## Stopper et détruire l'application

Pour arrêter les containers :
```bash
python Learnagement.py -stop
```

Pour détruire les containers et les données :
```bash
python Learnagement.py -destroy
```

## Problème récurent 

### Bug du phpMyAdmin : mauvais droits sur les fichiers

En allant sur phpMyAdmin, un message d'erreur peut apparaître mentionnant des permissions de fichier. Si c'est le cas, aller sur la console du container `learnagement_phpmyadmin` sur Docker Desktop et entrer la commande suivante :
```bash
chmod 755 /etc/phpmyadmin/config.inc.php
```


Pour tout autre problème, se référer à la section [Issues](https://github.com/FlavienVernier/learnagement/issues).
