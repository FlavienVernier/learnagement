<?php
try {
    [
        "email" => $email,
        "password" => $password,
        "confirm" => $confirm,
    ] = $_POST;

    if (empty($password) || empty($confirm) || $password !== $confirm)
        redirect("login");

    $type = $_SESSION['type'];
    $sql = "UPDATE LNM_$type SET password = '".password_hash($password, PASSWORD_DEFAULT)."', password_updated = 0 WHERE LNM_$type.mail = '$email'";
    $result = mysqli_query($conn, $sql);
    if(empty($result))
        redirect("login");

    $_SESSION["connecte"] = true;
    $_SESSION["mail"] = $email;
    redirect("dashboad");
} catch (Exception $e) {
    #todo: log
    redirect("login");
}