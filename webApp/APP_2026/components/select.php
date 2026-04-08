<?php
$options = $options ?? [];
$sizeClass = !empty($size) ? " select-" . htmlspecialchars($size) : "";
$wrapStyle = !empty($minWidth) ? ' style="min-width:' . htmlspecialchars($minWidth) . 'px"' : '';
?>

<div class="input-wrap"<?= $wrapStyle ?>>
    <?php if (!empty($label)): ?>
        <label class="input-label"><?= htmlspecialchars($label) ?></label>
    <?php endif; ?>
    
    <div class="select-wrap">
        <select class="select<?= $sizeClass ?>">
            <?php foreach ($options as $opt): ?>
                <option><?= htmlspecialchars($opt) ?></option>
            <?php endforeach; ?>
        </select>
        <span class="select-chevron">▾</span>
    </div>
</div>