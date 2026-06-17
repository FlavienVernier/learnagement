<?php
$avatars = $avatars ?? [];
?>

<div class="avatar-group">
    <?php foreach ($avatars as $avatar): ?>
        <?= $t->component("avatar", props: $avatar) ?>
    <?php endforeach; ?>
</div>