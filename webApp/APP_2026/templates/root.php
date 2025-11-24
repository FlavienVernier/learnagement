<?= render("components/hearder", ["title" => "Learnagement", "routes" => []]) ?>

<main class="grow flex flex-col">
    <?php if (file_exists("pages/$page/index.inc.php")) : ?>
        <?php render("pages/$page/index.inc", ["conn" => $conn]); ?>
    <?php else : ?>
        <?php render("pages/404/index.inc"); ?>
    <? endif; ?>
</main>

<?= render("components/footer", []) ?>