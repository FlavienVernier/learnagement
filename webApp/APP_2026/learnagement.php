<?php
    if (!isset($_SESSION)){
        session_start([
            'cookie_lifetime' => 86400,
        ]);
    }

    if (!isset($_SESSION["connecte"])){
        $_SESSION["connecte"] = false;
        $_SESSION["mail"] = "";
        $_SESSION["type"]=""; //etudiant ou enseignant ou administration
    }

    $defaultPage = $_SESSION["connecte"] ? "home" : "login";
    $page= !isset($_GET["page"]) ? $defaultPage : $_GET["page"];
?>

<?php require './utils/render.php' ?>
<?php include("./utils/connectDB.php"); ?>

<?= render("templates/hearder", ["title" => "Learnagement"]) ?>

<main class="grow flex flex-col">
    <?php if (file_exists("pages/$page/index.inc.php")) : ?>
        <?php include("pages/$page/index.inc.php"); ?>
    <?php else : ?>
        <?php include("pages/404/index.inc.php"); ?>
    <? endif; ?>
</main>

<?= render("templates/footer", []) ?>