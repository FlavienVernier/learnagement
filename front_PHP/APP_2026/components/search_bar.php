<?php
$value = $value ?? '';
$name = $name ?? 'q';
$placeholder = $placeholder ?? 'Rechercher…';
$size = $size ?? 'md';

$inputClass = "input" . ($size === 'lg' ? " input-lg" : "");
// Adjust padding dynamically for the large version
$inputStyle = ($size === 'lg') ? ' style="padding-left:44px; padding-right:44px"' : '';
$iconStyle = ($size === 'lg') ? ' style="left:14px"' : '';
$showClear = $showClear ?? true; // Default to showing the clear button
?>

<div class="search-bar">
    <span class="search-bar-icon"<?= $iconStyle ?>>
        <svg width="<?= $size === 'lg' ? '16' : '14' ?>" height="<?= $size === 'lg' ? '16' : '14' ?>" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="6.5" cy="6.5" r="4.5"/><path d="m10.5 10.5 3 3"/>
        </svg>
    </span>
    
    <input id="<?= $uuid ?>" type="search" name="<?= $name ?>"
        value="<?= $value ?>"
        class="<?= $inputClass ?>"
        placeholder="<?= htmlspecialchars($placeholder) ?>"
        <?= $inputStyle ?>>
</div>