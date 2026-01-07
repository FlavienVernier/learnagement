<?php
    $routes = [
        [ "link" => "home", "label" => "Acceuil", "img" => "./assets/icons/home.svg" ],
        [ "link" => "mobility_map", "label" => "Mobility Map", "img" => "./assets/icons/map.svg" ],
        [ "link" => "liste_personnel", "label" => "Liste", "img" => "./assets/icons/list.svg" ],
        [ "link" => "ressources", "label" => "Ressources", "img" => "./assets/icons/info.svg" ],
        [ "link" => "python", "label" => "Tableau de bord", "img" => "./assets/icons/console.svg" ],
    ];
    if ($_SESSION['type'] != 'administratif')
        array_push($routes, [ "link" => "rendus", "label" => "Mes Rendus", "img" => "./assets/icons/file.svg" ]);
    if ($_SESSION['type'] == 'etudiant')
        array_push($routes, [ "link" => $_SESSION["type"], "label" => "Mon compte", "img" => "./assets/icons/user-circle.svg" ]);
?>

<?= render("components/header", ["title" => "Learnagement", "routes" => $routes]) ?>

<main class="grow flex flex-col">
    <div class="grow flex lg:mx-4 lg:mt-4 lg:gap-4">
        <div class="hidden lg:flex items-center">
            <div class="bg-primary text-on-primary rounded-lg flex flex-col h-full gap-6 p-4 sticky group transition-all duration-200 ease-linear w-14 hover:w-48">
                <?php foreach ($routes as $route) { ?>
                    <a href="<?= router("home", ["section" => $route["link"]]) ?>" class="flex items-center gap-3 overflow-hidden whitespace-nowrap">
                        <div class="w-6 h-6 min-w-[1.5rem]">
                            <?php include($route["img"]) ?>
                        </div>
                        <p class="opacity-0 group-hover:opacity-100 transition-opacity duration-200 delay-50"><?= $route["label"] ?></p>
                    </a>
                <?php } ?>
            </div>
        </div>
        <div class="grow flex flex-col lg:shadow-xl lg:rounded p-4">
            <?php if (file_exists("pages/dashboard/$page/index.inc.php")) : ?>
                <?php render("pages/dashboard/$page/index.inc", ["conn" => $conn]); ?>
            <?php else : ?>
                <?php render("pages/404/index.inc"); ?>
            <? endif; ?>
        </div>
    </div>
</main>

<?= render("components/footer", []) ?>