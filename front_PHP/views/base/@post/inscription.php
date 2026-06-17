<?php
try {
    $t->router->redirect('login');
    /*
     * DEPRECATED Password management is out of front scop
     */
    /*
    [
        "email" => $email,
        "password" => $password,
        "confirm" => $confirm,
    ] = $_POST;

    if (empty($password) || empty($confirm) || $password !== $confirm)
        $t->router->redirect('login');

    $type = $_SESSION['type'];
    $sql = "UPDATE LNM_$type SET password = '".password_hash($password, PASSWORD_DEFAULT)."', password_updated = 0 WHERE LNM_$type.mail = '$email'";
    $result = mysqli_query($pdo, $sql);
    if(empty($result))
        $t->router->redirect('login');

    $_SESSION["connecte"] = true;
    $_SESSION["email"] = $email;
    $t->router->redirect('dashboard');
    */
} catch (Exception $e) {
    #todo: log
    $t->router->redirect('login');
}