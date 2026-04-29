<?php
function renderNavItem(array $item, int $depth = 0): void
{
    $indent = $depth > 0 ? 'pl-' . (8 + $depth * 4) : '';

    match ($item['type']) {
        'item'     => renderItem($item, $indent),
        'dropdown' => renderDropdown($item, $indent),
        default    => null,
    };
}

function renderItem(array $item, string $indent = ''): void { ?>
    <li>
        <a href="<?= htmlspecialchars($item['url'] ?? '#') ?>"
           class="flex items-center px-2 py-1.5 <?= $indent ?> text-body rounded-base hover:text-fg-brand group transition-colors">
            <?php if (!empty($item['icon'])): ?>
               <div class="w-5 h-5">
                  <?= $item['icon'] ?>
               </div>
            <?php endif; ?>
            <span class="ms-3"><?= htmlspecialchars($item['label']) ?></span>
        </a>
    </li>
<?php }

function renderDropdown(array $item, string $indent = ''): void
{
    $id = 'dropdown-' . md5($item['label']); ?>
    <li>
        <button type="button"
                class="flex items-center w-full justify-between px-2 py-1.5 <?= $indent ?> text-body rounded-base hover:text-fg-brand group transition-colors"
                aria-controls="<?= $id ?>"
                data-collapse-toggle="<?= $id ?>">
            <?php if (!empty($item['icon'])): ?>
               <div class="w-5 h-5">
                  <?= $item['icon'] ?>
               </div>
            <?php endif; ?>
            <span class="flex-1 ms-3 text-left rtl:text-right whitespace-nowrap">
                <?= htmlspecialchars($item['label']) ?>
            </span>
            <svg class="w-4 h-4 shrink-0" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 9-7 7-7-7"/>
            </svg>
        </button>
        <?php if (!empty($item['items'])): ?>
            <ul id="<?= $id ?>" class="hidden py-1 space-y-0.5">
                <?php foreach ($item['items'] as $child): ?>
                    <?php renderNavItem($child, 1) ?>
                <?php endforeach; ?>
            </ul>
        <?php endif; ?>
    </li>
<?php }
?>

<button  data-drawer-target="separator-sidebar" data-drawer-toggle="separator-sidebar" aria-controls="separator-sidebar" type="button"
   class="text-heading bg-primary text-on-primary box-border border border-transparent hover: focus:ring-4 focus:ring-neutral-tertiary font-medium leading-5 rounded-base text-sm p-2 focus:outline-none inline-flex sm:hidden">
   <span class="sr-only">Open sidebar</span>
   <svg class="w-6 h-6" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M5 7h14M5 12h14M5 17h10"/>
   </svg>
</button>

<aside id="separator-sidebar" class="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
   <div class="h-full px-3 py-4 overflow-y-auto bg-primary text-on-primary border-e border-default">
      <ul class="space-y-0.5 font-medium">
         <?php foreach ($urls as $url): ?>
            <?php if ($url['type'] === 'split'): ?>
               </ul>
               <ul class="space-y-2 font-medium border-t border-default pt-4 mt-4">
            <?php elseif ($url['type'] === 'item'): ?>
                  <?php renderNavItem($url) ?>

            <?php elseif ($url['type'] === 'section' && !empty($url['items'])): ?>
                  <li class="pt-4">
                     <span class="px-2 text-xs text-heading uppercase tracking-wider">
                        <?= htmlspecialchars($url['label']) ?>
                     </span>
                     <ul class="mt-1 space-y-0.5">
                        <?php foreach ($url['items'] as $item): ?>
                              <?php renderNavItem($item) ?>
                        <?php endforeach; ?>
                     </ul>
                  </li>
            <?php endif; ?>
         <?php endforeach; ?>
      </ul>
   </div>
</aside>