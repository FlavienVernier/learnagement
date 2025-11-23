<?php
    if (
        empty($_POST["mdp1"]) || empty($_POST["mdp2"]) || // MDP not send
        $_POST["mdp1"] != $_POST["mdp2"] // MDP1 != MDP2
    ) {
        redirect("login");
    }

    [
        "id" => $mail,
        "mdp1" => $mdp1,
        "mdp2" => $mdp2
    ] = $_POST;

    $type = $_SESSION['type'];
    $sql = "UPDATE LNM_$type SET password = '".password_hash($mdp1, PASSWORD_DEFAULT)."', password_updated = 0 WHERE LNM_$type.mail = '$mail'";
    $result = mysqli_query($conn, $sql);
    if(empty($result)) {
        redirect("login");
    }
    $_SESSION["connecte"] = true;
    $_SESSION["mail"] = $mail;
    redirect("home");