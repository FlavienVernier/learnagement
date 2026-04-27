<?php
// Core properties
$id = $id ?? null;
$label = $label ?? '';
$type = $type ?? 'button';

// Class modifiers
$variantClass = !empty($variant) ? " btn-" . htmlspecialchars($variant) : "";
$sizeClass = !empty($size) ? " btn-" . htmlspecialchars($size) : "";
$iconOnlyClass = (!empty($iconOnly) && $iconOnly === true) ? " btn-icon" : "";
$loadingClass = (!empty($loading) && $loading === true) ? " loading" : "";

$classes = "{$variantClass}{$sizeClass}{$iconOnlyClass}{$loadingClass}";

// Attributes
$disabledAttr = (!empty($disabled) && $disabled === true) ? " disabled" : "";
$tooltipAttr = !empty($tooltip) ? ' data-tooltip="' . htmlspecialchars($tooltip) . '"' : "";
$onclickAttr = !empty($onclick) ? ' onclick="' . htmlspecialchars($onclick) . '"' : "";

// Build the inner content
$content = '';
if (!empty($iconOnly) && $iconOnly === true) {
    $content = $label; 
} else {
    if (!empty($icon)) {
        $content .= "<span>" . $icon . "</span> ";
    }
    if (!empty($loading) && $loading === true) {
        $content .= '<span class="btn-label">' . $label . '</span>';
    } else {
        $content .= $label;
    }
}
?>

<button type="<?= htmlspecialchars($type) ?>" class="<?= trim($classes) ?>"<?= $disabledAttr ?><?= $tooltipAttr ?><?= $onclickAttr ?>>
    <?= $content ?>
</button>