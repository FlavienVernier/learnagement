<?php
// Modifiers and Attributes
$interactiveClass = (!empty($interactive) && $interactive === true) ? " card-interactive" : "";
$styleAttr = !empty($style) ? ' style="' . htmlspecialchars($style) . '"' : "";
$onclickAttr = !empty($onclick) ? ' onclick="' . htmlspecialchars($onclick) . '"' : "";
?>

<div class="card<?= $interactiveClass ?>"<?= $styleAttr ?><?= $onclickAttr ?>>
    
    <?php if (!empty($header)): ?>
        <div class="card-header">
            <?= $header ?>
        </div>
    <?php elseif (!empty($title)): ?>
        <div class="card-header">
            <span class="card-title"><?= htmlspecialchars($title) ?></span>
        </div>
    <?php endif; ?>

    <?php if (!empty($body)): ?>
        <div class="card-body">
            <?= $body ?>
        </div>
    <?php endif; ?>

    <?php if (!empty($footer)): ?>
        <div class="card-footer">
            <?= $footer ?>
        </div>
    <?php endif; ?>

</div>