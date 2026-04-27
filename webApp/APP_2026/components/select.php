<?php
$options = $options ?? [];
$sizeClass = !empty($size) ? " select-" . htmlspecialchars($size) : "";
$wrapStyle = !empty($minWidth) ? ' style="min-width:' . htmlspecialchars($minWidth) . 'px"' : '';
$selectId = !empty($id) ? ' id="' . htmlspecialchars($id) . '"' : '';
$defaultText = $defaultText ?? "Sélectionnez une ou plusieurs options";
?>

<div class="input-wrap"<?= $wrapStyle ?>>
    <?php if (!empty($label)): ?>
        <label class="input-label"><?= htmlspecialchars($label) ?></label>
    <?php endif; ?>
    
    <div class="select-wrap">
        <select<?= $selectId ?> class="select<?= $sizeClass ?>">
            <option value="<?= htmlspecialchars($defaultText) ?>" selected><?= htmlspecialchars($defaultText) ?></option>
            <?php foreach ($options as $opt): ?>
                <option><?= htmlspecialchars($opt) ?></option>
            <?php endforeach; ?>
        </select>
        <span class="select-chevron">▾</span>
    </div>
</div>