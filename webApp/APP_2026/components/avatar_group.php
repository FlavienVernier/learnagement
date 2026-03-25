<?php
$avatars = $avatars ?? [];
?>

<div class="avatar-group">
    <?php foreach ($avatars as $avatar): ?>
        <?= render("components/avatar", $avatar) ?>
    <?php endforeach; ?>
</div>