<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Gestion des stages — Learnagement<?php $t->endSlot(); ?>

<?php

    /////////////////
    // WARNING !!!!
    // Direct SQL queries are deprecated. Use backend API endpoints instead.
    /////////////////

    $token = $user["jwt_token"];
    $id = $user['id'];

    function groupBy(array $items, string $key): array {
        $grouped = [];
        foreach ($items as $item) {
            if (!isset($item[$key])) {
                continue;
            }
            $grouped[$item[$key]][] = $item;
        }
        return $grouped;
    }
    
    // Get student info
    $student = get_etudiant($token, $id)[0];

    // Get polypoints info
    $polypoints = get_polypoints($token, $id);

    // Get stages info
    $stages = get_stages_etudiant($token, $id);
?>

<?php $t->startSlot('content'); ?>
<!-- En-tête profil -->
<div class="flex items-center gap-4 mb-8">
    <div class="w-14 h-14 rounded-full bg-blue-600 flex items-center justify-center text-white text-xl font-medium shrink-0">
        <?= strtoupper(mb_substr($student['prenom'], 0, 1) . mb_substr($student['nom'], 0, 1)) ?>
    </div>
    <div>
        <h1 class="text-2xl font-medium text-[#0f2744]">
            <?= htmlspecialchars($student['prenom']) ?> <?= htmlspecialchars($student['nom']) ?>
        </h1>
        <div class="flex items-center gap-2 mt-1">
            <span class="text-sm text-slate-500"><?= htmlspecialchars($student['nom_filiere']) ?></span>
            <span class="text-slate-300">·</span>
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-800">
                <?= htmlspecialchars($student['nom_statut']) ?>
            </span>
        </div>
    </div>
</div>



    <!-- POLYPOINTS -->
<section class="mb-8">

    <div class="flex items-center justify-between mb-4">
        <h2 class="text-base font-medium text-[#0f2744]">Polypoints</h2>
        <span class="text-xs text-slate-400"><?= count($polypoints) ?> entrée<?= count($polypoints) > 1 ? 's' : '' ?></span>
    </div>

    <!-- Résumé par année -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mb-5">
        <?php foreach (groupBy($polypoints, 'annee_universitaire') as $annee => $points): ?>
            <div class="bg-white border border-black/8 rounded-xl p-4">
                <p class="text-xs text-slate-500 mb-1">Année <?= htmlspecialchars($annee) ?></p>
                <p class="text-2xl font-medium text-[#0f2744]"><?= array_sum(array_column($points, 'nb_point')) ?></p>
                <p class="text-xs text-slate-400 mt-0.5">polypoints enregistrés</p>
            </div>
        <?php endforeach; ?>
    </div>

    <!-- Tableau -->
    <div class="bg-white border border-black/8 rounded-xl overflow-hidden">
        <div class="overflow-x-auto">
            <table class="w-full text-sm border-collapse">
                <thead>
                    <tr class="border-b border-black/8 bg-slate-50">
                        <th class="px-4 py-3 text-left text-xs font-medium text-slate-500">Action</th>
                        <th class="px-4 py-3 text-left text-xs font-medium text-slate-500">Détail</th>
                        <th class="px-4 py-3 text-center text-xs font-medium text-slate-500">Points</th>
                        <th class="px-4 py-3 text-left text-xs font-medium text-slate-500">Année</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($polypoints as $point): ?>
                        <tr class="border-b border-black/5 last:border-0 hover:bg-slate-50 transition-colors">
                            <td class="px-4 py-3 text-[#0f2744]"><?= htmlspecialchars($point['intitule']) ?></td>
                            <td class="px-4 py-3 text-slate-500"><?= htmlspecialchars($point['tache']) ?></td>
                            <td class="px-4 py-3 text-center">
                                <span class="inline-flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium
                                    <?= $point['nb_point'] > 0 ? 'bg-blue-50 text-blue-800' : 'bg-red-50 text-red-800' ?>">
                                    <?= $point['nb_point'] > 0 ? '+' : '' ?><?= $point['nb_point'] ?>
                                </span>
                            </td>
                            <td class="px-4 py-3 text-slate-500"><?= htmlspecialchars($point['annee_universitaire']) ?></td>
                        </tr>
                    <?php endforeach; ?>
                    <?php if (empty($polypoints)): ?>
                        <tr>
                            <td colspan="4" class="px-4 py-8 text-center text-sm text-slate-400">Aucun polypoint enregistré</td>
                        </tr>
                    <?php endif; ?>
                </tbody>
            </table>
        </div>
    </div>

</section>

<!-- STAGES -->
<section>

    <div class="flex items-center justify-between mb-4">
        <h2 class="text-base font-medium text-[#0f2744]">Stages</h2>
        <span class="text-xs text-slate-400"><?= count($stages) ?> stage<?= count($stages) > 1 ? 's' : '' ?></span>
    </div>

    <?php if (empty($stages)): ?>
        <div class="bg-white border border-black/8 rounded-xl px-4 py-8 text-center text-sm text-slate-400">
            Aucun stage enregistré
        </div>
    <?php else: ?>

        <!-- Cards stages -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-5">
            <?php foreach ($stages as $stage):
                error_log($stage['date_debut'] . " " . $stage['date_fin']);
                $debut = DateTime::createFromFormat('Y-m-d', $stage['date_debut']);
                $fin   = DateTime::createFromFormat('Y-m-d', $stage['date_fin']);
                $duree = $debut->diff($fin)->days;
            ?>
                <div class="bg-white border border-black/8 rounded-xl p-4">
                    <div class="flex items-start justify-between gap-3 mb-3">
                        <div>
                            <p class="text-sm font-medium text-[#0f2744]"><?= htmlspecialchars($stage['entreprise']) ?></p>
                            <p class="text-xs text-slate-500 mt-0.5"><?= htmlspecialchars($stage['nature']) ?></p>
                        </div>
                        <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-50 text-green-800 shrink-0 whitespace-nowrap">
                            <?= $duree ?> jours
                        </span>
                    </div>
                    <div class="flex items-center gap-1.5 text-xs text-slate-400">
                        <svg width="12" height="12" fill="none" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.8"/><line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="1.8"/></svg>
                        <?= $debut->format('d/m/Y') ?> → <?= $fin->format('d/m/Y') ?>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>

        <!-- Tableau -->
        <div class="bg-white border border-black/8 rounded-xl overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-sm border-collapse">
                    <thead>
                        <tr class="border-b border-black/8 bg-slate-50">
                            <th class="px-4 py-3 text-left text-xs font-medium text-slate-500">Entreprise</th>
                            <th class="px-4 py-3 text-left text-xs font-medium text-slate-500">Nature</th>
                            <th class="px-4 py-3 text-left text-xs font-medium text-slate-500">Début</th>
                            <th class="px-4 py-3 text-left text-xs font-medium text-slate-500">Fin</th>
                            <th class="px-4 py-3 text-center text-xs font-medium text-slate-500">Durée</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($stages as $stage):
                            $debut = DateTime::createFromFormat('Y-m-d', $stage['date_debut']);
                            $fin   = DateTime::createFromFormat('Y-m-d', $stage['date_fin']);
                            $duree = $debut->diff($fin)->days;
                        ?>
                            <tr class="border-b border-black/5 last:border-0 hover:bg-slate-50 transition-colors">
                                <td class="px-4 py-3 font-medium text-[#0f2744]"><?= htmlspecialchars($stage['entreprise']) ?></td>
                                <td class="px-4 py-3 text-slate-500"><?= htmlspecialchars($stage['nature']) ?></td>
                                <td class="px-4 py-3 text-slate-500"><?= $debut->format('d/m/Y') ?></td>
                                <td class="px-4 py-3 text-slate-500"><?= $fin->format('d/m/Y') ?></td>
                                <td class="px-4 py-3 text-center">
                                    <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-50 text-green-800">
                                        <?= $duree ?> j
                                    </span>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>

    <?php endif; ?>

</section>
<?php $t->endSlot(); ?>