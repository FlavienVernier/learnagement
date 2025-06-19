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
  //$base_dir = ereg_replace("(/public_html).*", "\\1",$_SERVER['SCRIPT_FILENAME']);
  //$base_dir = preg_replace("/public_html#", "\\1",$_SERVER['SCRIPT_FILENAME']);
  //$base_dir = "/home/flver/public_html";
  //print($base_dir);

// construction du chemin pour le répertoire include
  //$inc_dir = $base_dir."/include/";

// inclusion des informations de connexion à la base de données MySQL
  //include($inc_dir."mysql_inc.php");


// Session timeout in second
  $session_timeout = 900;


//$mysql_server = "127.0.0.1";
$mysql_server = "mysql";
//$mysql_user = "learnagement";
$mysql_user = "root";
//$mysql_passwd = "LMent2Change";
$mysql_passwd = "Root2Change";
$mysql_db = "learnagement";
$mysql_port = "3306";
//$mysql_port = "43306";

$sessionId = "None";
$vue_name = "None";
$table_name = "None";
$fields = "None";
$reference_table_name="";
$primaryk_and_secondaryK="";
$userlogin="";
?>
