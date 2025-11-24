<?php
function render($template, $vars = []) {
    extract($vars);
    require __DIR__ . "/../$template.php";
    return ob_get_clean();
}