<?php
    $section = !isset($_GET["section"]) ? "agenda" : $_GET["section"];
?>

<div class="grow flex">
    <div class="hidden lg:flex items-center">
        <div class="bg-primary text-on-primary rounded-lg flex flex-col gap-4 p-2 m-2">
            <div class="w-8 h-8">
                <?php include("./assets/github-mark.svg") ?>
            </div>
            <div class="w-8 h-8">
                <?php include("./assets/github-mark.svg") ?>
            </div>
        </div>
    </div>
    <div class="grow">
        <?php if (file_exists("html_css/page_$section.inc.php")) : ?>
            <?php include("html_css/page_$section.inc.php"); ?>
        <?php else : ?>
            <?php include("pages/404/index.inc.php"); ?>
        <? endif; ?>
    </div>
</div>