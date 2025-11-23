<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <?php if (!empty($title)) : ?>
        <title><?= htmlspecialchars($title) ?></title>
    <? endif; ?>
    <?php include "./utils/router.php" ?>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="stylesheet" href="theme/theme.css">
    <link rel="stylesheet" href="theme/tailwind.extension.css">
</head>
<body class="flex flex-col min-h-screen">
    <header class="bg-primary text-on-primary">
        <nav aria-label="Global" class="flex items-center justify-between p-6 lg:px-8">
            <div class="flex lg:flex-1 gap-2">
                <a href="<?= router() ?>" class="h-10 w-30">
                    <?php include "assets/Logo_Polytech_Annecy_Chambery.svg"; ?>
                </a>
            </div>
            <div class="flex lg:hidden">
                <button type="button" command="show-modal" commandfor="mobile-menu" class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5">
                    <span class="sr-only">Open main menu</span>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" data-slot="icon" aria-hidden="true" class="size-6">
                        <path d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                </button>
            </div>

            <div class="hidden lg:flex lg:flex-1 gap-4 lg:justify-end">
                <?php if (isset($_SESSION['connecte']) && $_SESSION['connecte']): ?>
                    <a href="<?= router("home", ["section" => $_SESSION["type"]]) ?>" class="text-sm/6 font-semibold"><?= htmlspecialchars($_SESSION['mail'] ?? '') ?></a>
                    <a href="<?= router("logout") ?>" class="text-sm/6 font-semibold">Se déconnecter <span aria-hidden="true">&rarr;</span></a>
                <?php else: ?>
                    <a href="<?= router("login") ?>" class="text-sm/6 font-semibold">Se connecter <span aria-hidden="true">&rarr;</span></a>
                <?php endif; ?>
            </div>
        </nav>
        <el-dialog>
            <dialog id="mobile-menu" class="backdrop:bg-transparent lg:hidden">
                <div tabindex="0" class="fixed inset-0 focus:outline-none">
                    <el-dialog-panel class="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-white p-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
                        <div class="flex items-center justify-between">
                            <a href="<?= router() ?>" class="h-10 w-30">
                                <?php include "assets/Logo_Polytech_Annecy_Chambery.svg"; ?>
                            </a>
                            <button type="button" command="close" commandfor="mobile-menu" class="-m-2.5 rounded-md p-2.5 text-gray-700">
                                <span class="sr-only">Close menu</span>
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" data-slot="icon" aria-hidden="true" class="size-6">
                                    <path d="M6 18 18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" />
                                </svg>
                            </button>
                        </div>

                        <div class="mt-6 flow-root">
                            <div class="-my-6 flex flex-col divide-y divide-gray-500/10">
                                <?php if (isset($_SESSION['connecte']) && $_SESSION['connecte']): ?>
                                    <div class="space-y-2 py-6">
                                        <a href="<?= router("home", ["section" => $_SESSION["type"]]) ?>" class="-mx-3 block rounded-lg px-3 py-2 font-semibold">Mon Compte</a>
                                        <?php if ($_SESSION['type'] != 'administratif'): ?>
                                            <a href="<?= router("home", ["section" => "rendus_" . $_SESSION["type"]]) ?>" class="-mx-3 block rounded-lg px-3 py-2 font-semibold">Mes Rendus</a>
                                        <?php endif; ?>
                                        <a href="<?= router("home", ["section" => "dashboard_" . $_SESSION["type"]]) ?>" class="-mx-3 block rounded-lg px-3 py-2 font-semibold">Tableau de bord</a>
                                        <a href="<?= router("home", ["section" => "mobility_map"]) ?>" class="-mx-3 block rounded-lg px-3 py-2 font-semibold">Mobility Map</a>
                                        <a href="<?= router("home", ["section" => "liste_personnel"]) ?>" class="-mx-3 block rounded-lg px-3 py-2 font-semibold">Liste</a>
                                        <a href="<?= router("home", ["section" => "ressources"]) ?>" class="-mx-3 block rounded-lg px-3 py-2 font-semibold">Ressources</a>
                                    </div>
                                <?php endif; ?>
                                <div class="py-6 gap-2 flex flex-col">
                                    <?php if (isset($_SESSION['connecte']) && $_SESSION['connecte']): ?>
                                        <div class="place-self-end">
                                            <a href="<?= router("logout") ?>" class="text-sm/6 font-semibold"><?= htmlspecialchars($_SESSION['mail'] ?? '') ?></a>
                                        </div>
                                    <?php endif ?>
                                    <div class="place-self-end">
                                        <?php if (isset($_SESSION['connecte']) && $_SESSION['connecte']): ?>
                                            <a href="<?= router("logout") ?>" class="text-sm/6 font-semibold">Se déconnecter <span aria-hidden="true">&rarr;</span></a>
                                        <?php else: ?>
                                            <a href="<?= router("login") ?>" class="text-sm/6 font-semibold">Se connecter <span aria-hidden="true">&rarr;</span></a>
                                        <?php endif; ?>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </el-dialog-panel>
                </div>
            </dialog>
        </el-dialog>
    </header>