<?php
// Default values if none are provided
$type = $type ?? 'info';
$message = $message ?? '';

// Define default icons and titles for each alert type
$defaults = [
    'info'    => ['icon' => 'ℹ', 'title' => 'Information'],
    'success' => ['icon' => '✓', 'title' => 'Succès'],
    'warning' => ['icon' => '⚠', 'title' => 'Attention'],
    'error'   => ['icon' => '✕', 'title' => 'Erreur'],
];

// Use provided overrides, or fall back to the defaults
$icon = $icon ?? ($defaults[$type]['icon'] ?? 'ℹ');
$title = $title ?? ($defaults[$type]['title'] ?? '');
?>

<div class="alert alert-<?= htmlspecialchars($type) ?>">
    <span class="alert-icon"><?= htmlspecialchars($icon) ?></span>
    <div class="alert-body">
        <?php if (!empty($title)): ?>
            <div class="alert-title"><?= htmlspecialchars($title) ?></div>
        <?php endif; ?>
        
        <?= htmlspecialchars($message) ?>
    </div>
</div>