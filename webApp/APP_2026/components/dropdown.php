<?php
$id = $id ?? 'dropdown-' . uniqid();
$alignRight = (!empty($alignRight) && $alignRight === true) ? ' align-right' : '';
$label = $label ?? 'Menu ▾';
$items = $items ?? [];
?>

<div class="dropdown" id="<?= htmlspecialchars($id) ?>">
    <button
        class="btn btn-secondary"
        onclick="toggleDropdown(event, '<?= htmlspecialchars($id) ?>')"
    >
        <?= $label ?>
    </button>

    <div class="dropdown-menu<?= $alignRight ?>" id="<?= htmlspecialchars($id) ?>-menu">
        <?php foreach ($items as $item): ?>
            <?php if (($item['type'] ?? '') === 'label'): ?>
                <div class="dropdown-label"><?= htmlspecialchars($item['label']) ?></div>

            <?php elseif (($item['type'] ?? '') === 'divider'): ?>
                <div class="dropdown-divider"></div>

            <?php else: ?>
                <?php $dangerClass = (!empty($item['danger']) && $item['danger'] === true) ? ' danger' : ''; ?>
                <div class="dropdown-item<?= $dangerClass ?>">
                    <?php if (!empty($item['icon'])): ?>
                        <span class="item-icon"><?= $item['icon'] ?></span>
                    <?php endif; ?>
                    <?= htmlspecialchars($item['label'] ?? '') ?>
                </div>
            <?php endif; ?>
        <?php endforeach; ?>
    </div>
     <script>
        function toggleDropdown(event, id) {
            event.stopPropagation();
            const menu = document.getElementById(id + '-menu');
            if (!menu) return;
            const isOpen = menu.classList.contains('open');
            document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
            if (!isOpen) menu.classList.add('open');
        }

        document.addEventListener('click', e => {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu.open').forEach(m => m.classList.remove('open'));
            }
        });
    </script>
</div>