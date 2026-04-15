<?php
// Default to 'text' if no type is provided
$type = $type ?? 'text';

// Modifiers and Attributes
$typeClass = " skeleton-" . htmlspecialchars($type);
$styleAttr = !empty($style) ? ' style="' . htmlspecialchars($style) . '"' : '';
?>

<div class="skeleton<?= $typeClass ?>"<?= $styleAttr ?>></div>