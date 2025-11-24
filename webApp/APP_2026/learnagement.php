<?php
    require './utils/session.php';
    require './utils/render.php';
    include "./utils/connectDB.php";
    include "./utils/router.php";

    create_session();
    $defaultPage = $_SESSION["connecte"] ? "home" : "login";
    $page= !isset($_GET["page"]) ? $defaultPage : $_GET["page"];
    $section = !isset($_GET["section"]) ? "python" : $_GET["section"];

    // You can switch template here
    if($page === "home")
        render("templates/dashboard", ["page" => $section, "conn" => $conn]);
    else
        render("templates/root", ["page" => $page, "conn" => $conn]);