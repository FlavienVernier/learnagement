<?php
    if (isset($_POST["mdp1"]) && isset($_POST["mdp2"])){
        if ($_POST["mdp1"] == $_POST["mdp2"]){
            if($_SESSION['type'] == 'etudiant'){
                $sql = "UPDATE LNM_etudiant SET password = '".password_hash($_POST["mdp1"], PASSWORD_DEFAULT)."', password_updated = NOW() WHERE LNM_etudiant.mail = '".$_POST['id']."'";
                $result = mysqli_query($conn, $sql);
                if (!$result){
                    $_SESSION['type'] = "";
                    echo "<script>alert('Erreur liée à la base de données... :c')</script>";
                    echo "<script>window.location.href='?page=connexion'</script>";
                }
                else{
                    $_SESSION["connecte"]=true;
                    $_SESSION["mail"]=$_POST["id"];
                }
            }
            else if($_SESSION['type'] == 'enseignant'){
                $sql = "UPDATE LNM_enseignant SET password = '".password_hash($_POST["mdp1"], PASSWORD_DEFAULT)."', password_updated = NOW() WHERE LNM_enseignant.mail = '".$_POST['id']."'";
                $result = mysqli_query($conn, $sql);
                if (!$result){
                    $_SESSION['type'] = "";
                    echo "<script>alert('Erreur liée à la base de données... :c')</script>";
                    echo "<script>window.location.href='?page=connexion'</script>";
                }
                else{
                    $_SESSION["connecte"]=true;
                    $_SESSION["mail"]=$_POST["id"];
                }
            }
            else{
                $sql = "UPDATE LNM_administratif SET password = '".password_hash($_POST["mdp1"], PASSWORD_DEFAULT)."', password_updated = NOW() WHERE LNM_administratif.mail = '".$_POST['id']."'";
                $result = mysqli_query($conn, $sql);
                if (!$result){
                    $_SESSION['type'] = "";
                    echo "<script>alert('Erreur liée à la base de données... :c')</script>";
                    echo "<script>window.location.href='?page=connexion'</script>";
                }
                else{
                    $_SESSION["connecte"]=true;
                    $_SESSION["mail"]=$_POST["id"];
                }
            }
            echo "<script>alert('Changement de mot de passe réussi ! :)')</script>";
            echo "<script>window.location.href='?page=accueil'</script>";
            }
    }
    else{
        echo "<script>alert('Les mots de passe ne sont pas identiques ! :c')</script>";
        echo "<script>window.location.href='?page=connexion'</script>";
    }
?>
