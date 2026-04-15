<?php $t->extend('layouts/global'); ?>

<?php $t->startSlot('body'); ?>
<?php
    $urls = [
        ["type" => "item", "label" => "Dashboard", "url" => $t->router->href('dashboard'), "icon" => $t->asset('icons/square2x2.svg')],
        ["type" => "section", "label" => "Principale", "items" => []],
        ["type" => "section", "label" => "Professeur", "items" => []],
        ["type" => "section", "label" => "Administration", "items" => [
            ["type" => "dropdown", "label" => "Stage", "icon" => $t->asset('icons/company.svg'), "items" => [
                ["type" => "item", "label" => "Gérer les stages", "url" => $t->router->href('dashboard-stage')],
                ["type" => "item", "label" => "Nouveau stage",    "url" => $t->router->href('home')],
            ]],
            ["type" => "item", "label" => "Ressources", "url" => $t->router->href('dashboard-ressource'), "icon" => $t->asset('icons/file.svg')],
            ["type" => "item", "label" => "Carte de mobilité", "url" => $t->router->href('dashboard-mobility-map'), "icon" => $t->asset('icons/map.svg')],
        ]],
        ["type" => "split"],
        ["type" => "item", "label" => "Ancien Dashboard", "url" => $t->router->href('dashboard-python'), "icon" => $t->asset('icons/console.svg')],
        ["type" => "item", "label" => "Déconnexion", "url" => $t->router->href('logout'), "icon" => $t->asset('icons/out-door.svg')],
    ];

    if ($user && $user['type'] === 'etudiant') {
        $urls[1]['items'][] = ["type" => "item", "label" => "Profil", "url" => $t->router->href('dashboard-profile'), "icon" => $t->asset('icons/user-circle.svg')];
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