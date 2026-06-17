<?php
// Default values
$label = $label ?? '';
$colorClass = !empty($color) ? " badge-" . htmlspecialchars($color) : "";
$dotClass = (!empty($dot) && $dot === true) ? " badge-dot" : "";
?>

<span class="badge<?= $colorClass ?><?= $dotClass ?>">
    <?= htmlspecialchars($label) ?>
</span>