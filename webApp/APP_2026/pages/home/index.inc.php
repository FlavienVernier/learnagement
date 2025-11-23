<?php
    $section = !isset($_GET["section"]) ? "agenda" : $_GET["section"];
?>

<div class="grow flex lg:m-4 lg:gap-4">
    <div class="hidden lg:flex items-center">
        <div class="bg-primary text-on-primary rounded-lg flex flex-col h-full gap-6 p-2 sticky group">
            <a href="<?= router("home", ["section" => $_SESSION["type"]]) ?>" class="flex items-center gap-3">
                <div class="w-8 h-8">
                    <?php include("./assets/icons/user-circle.svg") ?> <!-- Mon Compte -->
                </div>
                <p class="hidden group-hover:block">Mon compte</p>
            </a>
            <?php if ($_SESSION['type'] != 'administratif'): ?>
                <a href="<?= router("home", ["section" => "rendus_" . $_SESSION["type"]]) ?>" class="flex items-center gap-3">
                    <div class="w-8 h-8">
                        <?php include("./assets/icons/user-circle.svg") ?> <!-- Mes Rendus -->
                    </div>
                    <p class="hidden group-hover:block">Mes Rendus</p>
                </a>
            <?php endif; ?>
            <a href="<?= router("home", ["section" => "dashboard"]) ?>" class="flex items-center gap-3">
                <div class="w-8 h-8">
                    <?php include("./assets/icons/map.svg") ?>  <!-- Tableau de bord -->
                </div>
                <p class="hidden group-hover:block">Tableau de bord</p>
            </a>
            <a href="<?= router("home", ["section" => "mobility_map"]) ?>" class="flex items-center gap-3">
                <div class="w-8 h-8">
                    <?php include("./assets/icons/map.svg") ?>  <!-- Mobility Map -->
                </div>
                <p class="hidden group-hover:block">Mobility Map</p>
            </a>
            <a href="<?= router("home", ["section" => "liste_personnel"]) ?>" class="flex items-center gap-3">
                <div class="w-8 h-8">
                    <?php include("./assets/icons/map.svg") ?>  <!-- Liste -->
                </div>
                <p class="hidden group-hover:block">Liste</p>
            </a>
            <a href="<?= router("home", ["section" => "ressources"]) ?>" class="flex items-center gap-3">
                <div class="w-8 h-8">
                    <?php include("./assets/icons/map.svg") ?>  <!-- Ressources -->
                </div>
                <p class="hidden group-hover:block">Ressources</p>
            </a>
        </div>
    </div>
    <div class="grow flex flex-col lg:shadow-xl lg:rounded p-4">
        <?php if (file_exists("pages/$section/index.inc.php")) : ?>
            <?php include("pages/$section/index.inc.php"); ?>
        <?php else : ?>
            <?php include("pages/404/index.inc.php"); ?>
        <? endif; ?>
    </div>
</div>