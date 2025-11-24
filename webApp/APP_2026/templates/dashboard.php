<?php
    $routes = [
        [ "link" => $_SESSION["type"], "label" => "Mon compte", "img" => "./assets/icons/user-circle.svg" ],
        [ "link" => "dashboard", "label" => "Tableau de bord", "img" => "./assets/icons/user-circle.svg" ],
        [ "link" => "mobility_map", "label" => "Mobility Map", "img" => "./assets/icons/user-circle.svg" ],
        [ "link" => "liste_personnel", "label" => "Liste", "img" => "./assets/icons/user-circle.svg" ],
        [ "link" => "ressources", "label" => "Ressources", "img" => "./assets/icons/user-circle.svg" ],
    ];
    if ($_SESSION['type'] != 'administratif')
        array_push($routes, [ "link" => "rendus_". $_SESSION["type"], "label" => "Mes Rendus", "img" => "./assets/icons/user-circle.svg" ]);
?>

<?= render("components/hearder", ["title" => "Learnagement", "routes" => $routes]) ?>

<main class="grow flex flex-col">
    <div class="grow flex lg:mx-4 lg:mt-4 lg:gap-4">
        <div class="hidden lg:flex items-center">
            <div class="bg-primary text-on-primary rounded-lg flex flex-col h-full gap-6 p-4 sticky group">
                <?php foreach ($routes as $route) { ?>
                    <a href="<?= router("home", ["section" => $route["link"]]) ?>" class="flex items-center gap-3">
                        <div class="w-6 h-6">
                            <?php include($route["img"]) ?>
                        </div>
                        <p class="hidden group-hover:block"><?= $route["label"] ?></p>
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