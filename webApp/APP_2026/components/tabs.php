<?php
$tabs = $tabs ?? [];
$typeClass = (!empty($type) && $type === 'pill') ? ' tabs-pill' : '';
$styleAttr = !empty($style) ? ' style="' . htmlspecialchars($style) . '"' : '';

// Create a default group ID if one isn't provided, so the JS still works
$groupId = $groupId ?? 'tab-group-' . uniqid();
?>

<div class="tabs<?= $typeClass ?>" role="tablist"<?= $styleAttr ?>>
    <?php foreach ($tabs as $tab): ?>
        <?php
        $isActive = (!empty($tab['active']) && $tab['active'] === true) ? ' active' : '';
        // Allow custom onclick, otherwise default to the setTab function from your JS
        $onclick = !empty($tab['onclick']) ? $tab['onclick'] : "setTab(this, '" . htmlspecialchars($groupId) . "')";
        $label = htmlspecialchars($tab['label'] ?? '');
        ?>
        <button class="tab<?= $isActive ?>" onclick="<?= $onclick ?>">
            <?= $label ?>
        </button>
    <?php endforeach; ?>
</div>