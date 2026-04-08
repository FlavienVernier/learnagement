<?php
$id = $id ?? 'search-' . uniqid(); // Ensure it always has an ID for the clear button
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
    
    <input type="search" class="<?= $inputClass ?>" placeholder="<?= htmlspecialchars($placeholder) ?>" id="<?= $id ?>"<?= $inputStyle ?>>
    
    <?php if ($showClear): ?>
        <button class="search-bar-clear" onclick="document.getElementById('<?= $id ?>').value=''; this.style.opacity=0;">✕</button>
    <?php endif; ?>
</div>