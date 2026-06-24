<?php $t->extend('layouts/global'); ?>

<?php $t->startSlot('body'); ?>
<?php
    $urls = [
        ["type" => "item", "label" => "Dashboard", "url" => $t->router->href('dashboard'), "icon" => $t->asset('icons/square2x2.svg')],
        ["type" => "section", "label" => "Principale", "items" => []],
        ["type" => "section", "label" => "Stages", "items" => []],
        ["type" => "section", "label" => "International", "items" => []],
        ["type" => "section", "label" => "Administration", "items" => [
            ["type" => "item", "label" => "Ressources", "url" => $t->router->href('dashboard-ressource'), "icon" => $t->asset('icons/file.svg')],
            ["type" => "item", "label" => "Annuaire", "url" => $t->router->href('dashboard-annuaire'), "icon" => $t->asset('icons/list.svg')],
        ]],
        ["type" => "split"],
        ["type" => "item", "label" => "Dashboard Dash-Plotly", "url" => $t->router->href('dashboard-python'), "icon" => $t->asset('icons/console.svg')],
        ["type" => "item", "label" => "Déconnexion", "url" => $t->router->href('logout'), "icon" => $t->asset('icons/out-door.svg')],
        ];
    if (getenv("ENV") == "prod"){
        $urls += [["type" => "item", "label" => "Dashboard NextJS", "url" => $t->router->href('dashboard-nextjs'), "icon" => $t->asset('icons/console.svg')]];
    }
        
    if ($user && $user['type'] === 'etudiant') {
        $urls[1]['items'][] = ["type" => "item", "label" => "Profil", "url" => $t->router->href('dashboard-profile'), "icon" => $t->asset('icons/user-circle.svg')];
        $urls[1]['items'][] = ["type" => "item", "label" => "Rendus", "url" => $t->router->href('dashboard-rendus-student'), "icon" => $t->asset('icons/file.svg')];
        $urls[3]['items'][] = ["type" => "item", "label" => "Carte de mobilité", "url" => $t->router->href('dashboard-mobility-map'), "icon" => $t->asset('icons/map.svg')];
    }
    /*if ($user && $user['type'] !== 'etudiant') {
        $urls[2]['items'][] = ["type" => "dropdown", "label" => "Stage", "icon" => $t->asset('icons/company.svg'), "items" => [
            ["type" => "item", "label" => "Gérer les stages", "url" => $t->router->href('dashboard-stage')],
            ["type" => "item", "label" => "Nouveau stage",    "url" => $t->router->href('dashboard-create-stage')],
        ]];
    }*/

    if ($user && $user['type'] === 'enseignant') {
        $urls[2]['items'][] = ["type" => "item", "label" => "Gérer les stages", "url" => $t->router->href('dashboard-stage'), "icon" => $t->asset('icons/company.svg')];
        // Not Yet operational
        //$urls[1]['items'][] = ["type" => "item", "label" => "Rendus", "url" => $t->router->href('dashboard-rendus-enseignant'), "icon" => $t->asset('icons/file.svg')];
    }

    if ($user && $user['type'] === 'administratif') {
        $urls[2]['items'][] = ["type" => "dropdown", "label" => "Stage", "icon" => $t->asset('icons/company.svg'), "items" => [
            ["type" => "item", "label" => "Gérer les stages", "url" => $t->router->href('dashboard-stage')],
            ["type" => "item", "label" => "Nouveau stage",    "url" => $t->router->href('dashboard-create-stage')],
        ]];
        $urls[3]['items'][] = ["type" => "item", "label" => "Gestion Mobilité (RI)", "url" => $t->router->href('dashboard-mobility-admin'), "icon" => $t->asset('icons/map.svg')];
    }
    if ($user && $user['type'] !== 'administratif') {
        $urls[1]['items'][] = ["type" => "item", "label" => "Dépendance Module",    "url" => $t->router->href('dashboard-dependance-module'), "icon" => $t->asset('icons/dependance_module.svg')];
    }
?>
<?= $t->slot('script.top') ?>
<main class="min-h-screen flex flex-col">
    <?= $t->component("sidebar", props: ["urls" => $urls]) ?>
    <div class="p-4 sm:ml-64 flex flex-col grow">
        <?= $t->slot('content', '<p class="p-8 text-gray-500">Aucun contenu.</p>') ?>
    </div>
</main>
<?= $t->slot('script.bottom') ?>
<?php $t->endSlot(); ?>