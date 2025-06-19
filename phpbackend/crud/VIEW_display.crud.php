<?php
function createVIEW_display($conn, $id_view, $sortIndex, $name, $group_of_views, $request) {
    $sql = "INSERT INTO `VIEW_display` (`id_view`, `sortIndex`, `name`, `group_of_views`, `request`) VALUES ('$id_view', '$sortIndex', '$name', '$group_of_views', '$request')";
    $res = mysqli_query($conn, $sql);
    return $res;
}

function deleteVIEW_display($conn, $id) {
    $sql = "DELETE FROM `VIEW_display` WHERE `id`=$id";
    $res = mysqli_query($conn, $sql);
    return $res;
}

function updateVIEW_display($conn, $id,$id_view, $sortIndex, $name, $group_of_views, $request) {
    $sql = "UPDATE `VIEW_display` SET `id_view`='$id_view', `sortIndex`='$sortIndex', `name`='$name', `group_of_views`='$group_of_views', `request`='$request' WHERE `id` = $id";
    $res = mysqli_query($conn, $sql);
    return $res;
}

function listVIEW_display($conn) {
    $sql = "SELECT * FROM `VIEW_display`";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res);
    return $rs;
}

function selectVIEW_display($conn, $id_view) {
    $sql = "SELECT * FROM `VIEW_display` WHERE `id_view`=$id_view";
    $res = mysqli_query($conn, $sql);
    $rs = rs_to_table($res)[0];
    return $rs;
}