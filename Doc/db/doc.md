# [General Normalization and spécific Normalisations](../doc.md)

## DB Normalization

### DB Naming

* Table: Table names should be nouns, in mixed case with the first letter of each internal word capitalized. Try to keep your table names simple and descriptive. Use whole words-avoid acronyms and abbreviations. Do not use special character
* Link Table: Whole 1st table name _as_ whole second table name (e.g., Foo_as_Bar)
* Attributs: Use whole words in lower case, acronyms and abbreviations in upper case and do not use special character
* Primary Key: id_ table name (e.g., id_Foo)
* Foreign Key: like its primary key (e.g., id_Foo), if the same primary key appear twise or more in the same table add _ specific name at the end (e.g., id_Foo_bar)
* View: GUI is automaticaly generated, according to the naming
	* user view for user GUI: VUE_ explicit vue name
	* learnings manager view for manager GUI: CHECK_  explicit vue name


### DB Constraints

Toutes les tables de données (hors table de liaisons) doivent avoir une clé primaire numérique composée d'un seul attribut et une clé secondaire composé d'un ensemble d'attributs humainement compréhensible.
Cet ensemble doit être déclaré comme unique avec pour nom d'indexe "SECONDARY".
Si la clé secondaire contient une clé étrangaire, la table concernée sera califiée d'intermédiaire.
La clé primaire est toujours constitué des premiers attributs, le premier dans le cas d'une table de base ou intermédiaire, les 2 premiers dans le cas d'une table de liaison.
Nous avons donc 3 types de table:
* les tables de base avec un seul attribut numérique clé primaire et une clé secondaire composée d'un ensemble d'attributs ne contemnant pas de clé étrangère 
* les tables intermédiaires avec un seul attribut numérique clé primaire et une clé secondaire composée d'un ensemble d'attributs contemnant au moins une clé étrangère  
* les tables de liaison avec 2 attributs formant la clé primaire et ne contenant pas de clé secondaire

### DB Files organisation

L'ensemble des fichiers de BD se placent dans les répertoires <GIT Repo>/freeData/ et <GIT Repo>/sql/.
The "freeData" directory contains free data used as examples or to texture the application. This directory is provided by git
The "sql" directory contains all sql scripts used to start the application, including links to data.
A "data" directory contains the data used to start the application is automatically created at start-up. This directory is private and must never be published.
Le nom des fichiers respecte la convention Flyway :

```V<version>__<description>.sql```

Le numéro de version se décompose en :

```<Project main release>.<DB evolution number>.<Execution order>```

La description débute par :
* struct_ : pour le SQL relatif à la structure de données de la base
* data_ : pour les données insérées dans les tables
* trigger_ : pour les triggers
* trim_ : pour supprimer, nettoyer et déprécier définitivement

**ATTENTION** : un fichier ```.sql``` ne doit **jamais** être modifié, toute modification de la BD implique un nouveau fichier ```.sql``` 

[Back](../doc.md)