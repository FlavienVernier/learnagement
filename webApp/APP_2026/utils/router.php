<?php
function router($page=null, $params = []) {
    if (empty($page))
        return "/APP_2026/learnagement.php";
    
    return "/APP_2026/learnagement.php?page=" . urlencode($page) . 
        (count($params) > 0 ? '&' . http_build_query($params) : '');
}

function redirect($page=null, $params = []) {
    $url = router($page, $params);
    echo "<script>window.location.href='$url'</script>";
    exit();
}