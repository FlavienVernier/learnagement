<?php
    $type = $_SESSION['type'];
    render("pages/dashboard/rendus/$type", ["conn" => $conn]);