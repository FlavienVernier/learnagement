<?php
$type = $type ?? 'text';
$id = !empty($id) ? ' id="' . htmlspecialchars($id) . '"' : '';
$value = isset($value) ? ' value="' . htmlspecialchars($value) . '"' : '';
$placeholder = !empty($placeholder) ? ' placeholder="' . htmlspecialchars($placeholder) . '"' : '';
$styleAttr = !empty($style) ? ' style="' . htmlspecialchars($style) . '"' : '';

// Classes
$sizeClass = !empty($size) ? " input-" . htmlspecialchars($size) : "";
$errorClass = (!empty($error) && $error === true) ? " error" : "";
$textareaClass = ($type === 'textarea') ? " textarea" : "";
$inputClass = "input{$sizeClass}{$errorClass}{$textareaClass}";

// Build the input tag
if ($type === 'textarea') {
    // Textarea ignores the value attribute and puts it inside the tags
    $inputHtml = "<textarea class=\"{$inputClass}\"{$id}{$placeholder}{$styleAttr}>" . htmlspecialchars($value ?? '') . "</textarea>";
} else {
    $inputHtml = "<input type=\"{$type}\" class=\"{$inputClass}\"{$id}{$value}{$placeholder}{$styleAttr}>";
}

// Wrap with icon if provided
if (!empty($icon)) {
    $inputHtml = '
    <div class="input-group">
        <span class="input-group-icon">' . $icon . '</span>
        ' . $inputHtml . '
    </div>';
}
?>

<div class="input-wrap" <?= !empty($wrapStyle) ? 'style="'.htmlspecialchars($wrapStyle).'"' : '' ?>>
    <?php if (!empty($label)): ?>
        <label class="input-label"><?= htmlspecialchars($label) ?></label>
    <?php endif; ?>

    <?= $inputHtml ?>

    <?php if (!empty($errorMsg)): ?>
        <span class="input-error-msg"><?= htmlspecialchars($errorMsg) ?></span>
    <?php elseif (!empty($hint)): ?>
        <span class="input-hint"><?= htmlspecialchars($hint) ?></span>
    <?php endif; ?>
</div>