<!DOCTYPE html>

<html>
<head>
    <title>Réinitialisation des mots de passe</title>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="style.css">
</head>

<body>
    <?php
        $message = "";

        require_once("../config.php");

        $conn = mysqli_connect("$_ENV['MYSQL_SERVER']","$_ENV['MYSQL_USER']","$_ENV['MYSQL_PASSWD']","$_ENV['MYSQL_DB']","$_ENV['MYSQL_PORT']")
        or die("Failed to connect to MySQL: " . mysqli_connect_error());

        set_time_limit(300);

        function motDePasse($longueur=8) { // 8 = longueur par défaut
            // chaine de caractères qui sera mis dans le désordre:
            $Chaine = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ&$%-_!?";
            // on mélange la chaine avec la fonction str_shuffle(), propre à PHP
            $Chaine = str_shuffle($Chaine);
            // ensuite on coupe à la longueur voulue avec la fonction substr(), propre à PHP aussi
            $Chaine = substr($Chaine,0,$longueur);
            // ensuite on retourne notre chaine aléatoire de "longueur" caractères:
            return $Chaine;
        }

        if (isset($_POST['id_admin']) && isset($_POST['mdp_admin'])) {

            if ($_POST['id_admin'] != $admin_user || $_POST['mdp_admin'] != $admin_passwd) {
                $message = "<p>Identifiant ou mot de passe incorrect.</p>";
            }
            else {
                // Génération et mise à jour des mots de passe des étudiants
                $sql = "SELECT mail FROM LNM_etudiant";
                $resultat = mysqli_query($conn, $sql) or die("Requête invalide: ". mysqli_error( $conn )."\n".$sql);

                while($ligne = mysqli_fetch_array($resultat)){
                    $nouveau_mdp = password_hash(motDePasse(), PASSWORD_DEFAULT);
                    $update_sql = "UPDATE LNM_etudiant SET password='$nouveau_mdp', password_updated=NULL WHERE mail=".$ligne['mail'];
                    mysqli_query($conn, $update_sql) or die("Requête invalide: ". mysqli_error( $conn )."\n".$update_sql);
                }

                // Génération et mise à jour des mots de passe des enseignants
                $sql = "SELECT mail FROM LNM_enseignant";
                $resultat = mysqli_query($conn, $sql) or die("Requête invalide: ". mysqli_error( $conn )."\n".$sql);

                while($ligne = mysqli_fetch_array($resultat)){
                    $nouveau_mdp = password_hash(motDePasse(), PASSWORD_DEFAULT);
                    $update_sql = "UPDATE LNM_enseignant SET password='$nouveau_mdp', password_updated=NULL WHERE mail=".$ligne['mail'];
                    mysqli_query($conn, $update_sql) or die("Requête invalide: ". mysqli_error( $conn )."\n".$update_sql);
                }

                $message = "<p>Les mots de passe ont été mis à jour avec succès.</p>";
            }
        }
    ?>
    <h1>Réinitialisation des mots de passe :</h1>
    <form method='post'><br>
        <input type='text' name='id_admin' placeholder='Identifiant'><br>
        <input type='password' name='mdp_admin' placeholder='Mot de passe'><br>
        <input type='submit' value='Valider'></input>
    </form>
    <?php
    if ($message != "") {
        echo $message;
    }
    ?>
</body>
</html>
