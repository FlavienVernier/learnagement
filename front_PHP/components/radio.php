<?php
// Attributes
$nameAttr = !empty($name) ? ' name="' . htmlspecialchars($name) . '"' : '';
$valueAttr = isset($value) ? ' value="' . htmlspecialchars($value) . '"' : '';
$checkedAttr = (!empty($checked) && $checked === true) ? ' checked' : '';
$disabledAttr = (!empty($disabled) && $disabled === true) ? ' disabled' : '';

// Styling for disabled state
$labelStyle = (!empty($disabled) && $disabled === true) ? ' style="opacity:.45"' : '';
?>

<label class="radio-wrap">
    <input type="radio"<?= $nameAttr ?><?= $valueAttr ?><?= $checkedAttr ?><?= $disabledAttr ?>>
    <?php if (!empty($label)): ?>
        <span class="radio-label"<?= $labelStyle ?>><?= htmlspecialchars($label) ?></span>
    <?php endif; ?>
</label>