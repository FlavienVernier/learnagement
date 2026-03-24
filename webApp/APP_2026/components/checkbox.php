<?php
// Attributes
$nameAttr = !empty($name) ? ' name="' . htmlspecialchars($name) . '"' : '';
$valueAttr = isset($value) ? ' value="' . htmlspecialchars($value) . '"' : '';
$checkedAttr = (!empty($checked) && $checked === true) ? ' checked' : '';
$disabledAttr = (!empty($disabled) && $disabled === true) ? ' disabled' : '';

// Styling for disabled state
$labelStyle = (!empty($disabled) && $disabled === true) ? ' style="opacity:.45"' : '';
?>

<label class="check-wrap">
    <input type="checkbox"<?= $nameAttr ?><?= $valueAttr ?><?= $checkedAttr ?><?= $disabledAttr ?>>
    <?php if (!empty($label)): ?>
        <span class="check-label"<?= $labelStyle ?>><?= htmlspecialchars($label) ?></span>
    <?php endif; ?>
</label>