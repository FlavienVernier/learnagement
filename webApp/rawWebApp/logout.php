<?php
// On démarre la session
session_start ();

session_regenerate_id(true);

// On détruit les variables de notre session
session_unset ();

unset($_SESSION["loggedin"]);

// On détruit notre session
session_destroy ();

// On redirige le visiteur vers la page d'accueil
header ('location: index.php');
?>
