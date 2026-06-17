<?php
// Default values
$size = $size ?? 'md';
$initials = $initials ?? '';
$colorClass = !empty($color) ? " avatar-" . htmlspecialchars($color) : "";
$tooltipAttr = !empty($tooltip) ? " data-tooltip=\"" . htmlspecialchars($tooltip) . "\"" : "";
?>

<div class="avatar avatar-<?= htmlspecialchars($size) ?><?= $colorClass ?>"<?= $tooltipAttr ?>>
    <?= htmlspecialchars($initials) ?>
</div>