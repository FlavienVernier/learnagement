<?php $t->extend('layouts/global'); ?>

<?php $t->startSlot('body'); ?>
<main class="min-h-screen flex flex-col">
    <?= $t->component("navbar", ['routes'=> [
        "Accueil" => $t->router->href('home'),
    ]]) ?>
    <section class="flex-1 flex flex-col">
        <?= $t->slot('content', '<p class="p-8 text-gray-500">Aucun contenu.</p>') ?>
    </section>
    <?= $t->component("footer") ?>
</main>
<?php $t->endSlot(); ?>