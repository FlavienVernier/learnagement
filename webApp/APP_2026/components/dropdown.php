<?php
$id = $id ?? 'dropdown-' . uniqid();
$alignRight = (!empty($alignRight) && $alignRight === true) ? " align-right" : "";
$items = $items ?? [];
?>

<div class="dropdown" id="<?= htmlspecialchars($id) ?>">
    <?= $trigger ?? '<button class="btn btn-secondary" onclick="toggleDropdown(\'' . htmlspecialchars($id) . '\')">Menu ▾</button>' ?>

    <div class="dropdown-menu<?= $alignRight ?>" id="<?= htmlspecialchars($id) ?>-menu">
        <?php foreach ($items as $item): ?>
            <?php if (($item['type'] ?? '') === 'label'): ?>
                <div class="dropdown-label"><?= htmlspecialchars($item['label']) ?></div>
                
            <?php elseif (($item['type'] ?? '') === 'divider'): ?>
                <div class="dropdown-divider"></div>
                
            <?php else: ?>
                <?php $dangerClass = (!empty($item['danger']) && $item['danger'] === true) ? " danger" : ""; ?>
                <div class="dropdown-item<?= $dangerClass ?>">
                    <?php if (!empty($item['icon'])): ?>
                        <span class="item-icon"><?= $item['icon'] ?></span>
                    <?php endif; ?>
                    <?= htmlspecialchars($item['label'] ?? '') ?>
                </div>
            <?php endif; ?>
        <?php endforeach; ?>
    </div>
</div>