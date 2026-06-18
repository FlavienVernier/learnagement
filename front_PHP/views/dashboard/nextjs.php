<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Dashboard NextJS— Learnagement<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>
<?php
    require_once("./config.php");
    loadEnv(".");

    $type = $_SESSION['type'];
?>

<?php
    $protocol = $_ENV['ENV'] === 'prod' ? 'https' : 'http';
    $protocol = 'http'; // https not yet supported by nextjs app
    $dash_url = $protocol . '://' . $_SERVER['SERVER_NAME'] . ':' . $_ENV['FRONT_NEXTAUTH_PORT'] . '/?jwt_token=' . $_SESSION["jwt_token"];

    header("Location: " . $dash_url);
    exit();
?>

<?php $t->endSlot(); ?>
