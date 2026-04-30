# **Installation Guide**

## **Prerequisites**

Avant le premier lancement de l'application, assurez-vous que tout les fichiers en '.sh' sont bien sous format 'LF' (Linux) et pas 'CRLF' (Windows).

## **Installation**

### Creer un envirronement virtuel Python 3.10 ou supérieur

```bash
python3 -m venv myenv
source myenv/bin/activate  # Sur Windows: myenv\Scripts\activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Lancement de l'application

```bash
python.exe .\Learnagement.py
```

### **Configuration de la base de données**

![image](.\ImagesMarkdown\EtapeLancement1.png)
Lors du lancement de l'application veillez à :

- Nommer votre instance ( ici dev )
- Entrer un mot de passe Root pour la BDD ( ici toto )
- Entrer un mot de passe pour le User de la BDD ( ici toto )
- Lorsque le ligne Then press enter apparait, copier et coller le fichier ```.\db\freeData\V0.0.5__data_small.```sql  dans le dossier ```.\db\data\``` puis appuyer sur "Enter" pour continuer le lancement de l'application.
  ![image](.\ImagesMarkdown\EtapeLancement2.png)

- Docker :
  ![image](.\ImagesMarkdown\EtapeLancement3.png)
  - Cliquer sur le Port utilisé par la phpmyadmin pour vérifier sont foncitonnement
  - Dans le cas d'une erreure tels que :
    ![image](.\ImagesMarkdown\EtapeLancement4.png)
    Aller dans le terminal ( Exec ) du container et tapper la commande :

    ```bash
    chmod 755 /etc/phpmyadmin/config.inc.php
    ```
  - Arreter l'application ( CTRL + C )
  - Utiliser la commande dans le terminal du programme :

    ```bash
    docker compose up
    ```
  - Redémarrer le container puis essayer de se connecter à phpmyadmin pour vérifier sont foncitonnement
     Username : learnagement
     Password : ( ici toto )
  - Verifier que le container suivant et bien lancé sinon le démarrer :
    ![image](.\ImagesMarkdown\EtapeLancement5.png)

  - Si necessaire apres connection à l'application web, relancer l'ensemble de container puis lancer la commande ```docker compose up -d``` 
  - Relancer le container learnagment_php_dev
