<?php
function render($template, $vars = []) {
    extract($vars);
    // ob_start();
    require __DIR__ . "/../$template.php";
    return ob_get_clean();
}