<?php
// Attributes
$nameAttr = !empty($name) ? ' name="' . htmlspecialchars($name) . '"' : '';
$valueAttr = isset($value) ? ' value="' . htmlspecialchars($value) . '"' : '';
$checkedAttr = (!empty($checked) && $checked === true) ? ' checked' : '';
$disabledAttr = (!empty($disabled) && $disabled === true) ? ' disabled' : '';
$onchangeAttr = !empty($onchange) ? ' onchange="' . htmlspecialchars($onchange) . '"' : '';

// Styling for disabled state (applies to track, thumb, and label)
$opacityStyle = (!empty($disabled) && $disabled === true) ? ' style="opacity:.45"' : '';
?>

<label class="toggle-wrap">
    <div class="toggle">
        <input type="checkbox"<?= $nameAttr ?><?= $valueAttr ?><?= $checkedAttr ?><?= $disabledAttr ?><?= $onchangeAttr ?>>
        <div class="toggle-track"<?= $opacityStyle ?>></div>
        <div class="toggle-thumb"<?= $opacityStyle ?>></div>
    </div>
    <?php if (!empty($label)): ?>
        <span class="toggle-label"<?= $opacityStyle ?>><?= htmlspecialchars($label) ?></span>
    <?php endif; ?>
</label>
<script>
    /* ── Toggle ── */
    function syncToggle(input) { 
        // Logic depends on your CSS, but usually just needs to trigger onchange 
        console.log('Toggle state:', input.checked);
    }
</script>