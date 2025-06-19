<?php
/*******************************************************************************
   Repérage du répertoire de base sur le serveur http et du répertoire 'include'
  qu'il contient.
  Les lignes qui suivent utilisent les expressions régulières (très pratiques 
  pour effectuer des recherches, extractions, modifications dans des chaînes de
  caractères). Ici on recherche dans le chemin complet du script le chemin  
  complet du dossier 'public_html' vu par le serveur. A partir de ce chemin,
  quelque soit le sous-répertoire dans lequel ce trouve ce script, le chemin
  exact du répertoire 'include' est reconstruit.
******************************************************************************/

//  disconnexion au serveur MySQL (sur le serveur webtest de l'ESIA

    mysqli_close($conn);

?>
