
<header class="sticky w-full z-20 top-0 start-0">
  <nav class="bg-primary text-on-primary">
      <div class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl p-4">
          <a href="<?= $t->router->href('home') ?>" class="flex items-center space-x-3 rtl:space-x-reverse">
            <div class="h-8 w-30">
              <?= $t->asset("Logo_Polytech_Annecy_Chambery.svg") ?>
            </div>
          </a>
          <div class="flex items-center space-x-6 rtl:space-x-reverse">
              <?php if (!isset($user)) : ?>
                <a href="<?= $t->router->href('login') ?>" class="text-sm font-medium text-fg-brand hover:underline">Login</a>
              <?php else : ?>
                <a href="<?= $t->router->href('logout') ?>" class="text-sm font-medium text-fg-brand hover:underline">Logout</a>
              <?php endif; ?>
          </div>
      </div>
  </nav>
  <?php if (!empty($routes)) : ?>
    <nav class="bg-white border-y border-default border-default">
        <div class="max-w-screen-xl px-4 py-3 mx-auto">
            <div class="flex items-center">
                <ul class="flex flex-row font-medium mt-0 space-x-8 rtl:space-x-reverse text-sm">
                    <li>
                        <?php foreach ($routes as $name => $url) : ?>
                            <a href="<?= $url ?>" class="text-heading hover:underline" aria-current="page"><?= $name ?></a>
                        <?php endforeach; ?>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
  <?php endif; ?>
</header>