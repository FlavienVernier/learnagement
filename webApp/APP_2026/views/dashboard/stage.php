<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Gestion des stages<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>

<?php
    /////////////////
    // WARNING !!!!
    // Direct SQL queries are deprecated. Use backend API endpoints instead.
    /////////////////

$sql = "SELECT e.id_enseignant, e.nom, e.prenom FROM LNM_enseignant e;";
$stmt = mysqli_prepare($pdo, $sql);
mysqli_stmt_execute($stmt);
$result = mysqli_stmt_get_result($stmt);
$enseignants = mysqli_fetch_all($result, MYSQLI_ASSOC);
usort($enseignants, function ($a, $b) {
    return strcmp($a['nom'], $b['nom']);
});

$sql = "SELECT 
            s.*,
            CONCAT(UPPER(e.nom), ' ', e.prenom) AS student_fullname,
            e.mail,
            CONCAT(f.nom_filiere, p.annee) AS filiere,
            CONCAT(UPPER(en.nom), ' ', en.prenom) AS teacher_fullname,
            en.mail AS teacher_mail,
            CASE
                WHEN s.id_stage IS NULL THEN 'no-internship'
                WHEN en.id_enseignant IS NULL THEN 'pending'
                ELSE 'completed'
            END AS status
        FROM LNM_etudiant e
        JOIN LNM_promo p ON p.id_promo = e.id_promo
        JOIN LNM_filiere f ON f.id_filiere = p.id_filiere
        LEFT JOIN LNM_stage s ON s.id_etudiant = e.id_etudiant
        LEFT JOIN LNM_enseignant en ON en.id_enseignant = s.id_enseignant;";
$stmt = mysqli_prepare($pdo, $sql);
mysqli_stmt_execute($stmt);
$result = mysqli_stmt_get_result($stmt);
$etudiants = mysqli_fetch_all($result, MYSQLI_ASSOC);

$total       = count($etudiants);
$sans_stage  = array_values(array_filter($etudiants, fn($e) => $e['status'] === 'no-internship'));
$sans_tuteur = array_values(array_filter($etudiants, fn($e) => $e['status'] === 'pending'));
$complets    = array_values(array_filter($etudiants, fn($e) => $e['status'] === 'completed'));

$filtre    = $_GET['filtre'] ?? 'tous';
$recherche = $_GET['q'] ?? '';
$filtre_enseignant = $_GET['id_enseignant'] ?? '';

$liste = match($filtre) {
    'sans_stage'  => $sans_stage,
    'sans_tuteur' => $sans_tuteur,
    'complet'     => $complets,
    default       => $etudiants,
};

if ($recherche !== '' || $filtre_enseignant !== '') {
    $liste = array_values(array_filter($liste, function($e) use ($recherche, $filtre_enseignant) {
        // Filtre enseignant — doit correspondre exactement si renseigné
        if ($filtre_enseignant !== '' && (string)($e['id_enseignant'] ?? '') !== $filtre_enseignant)
            return false;

        // Filtre recherche — au moins un champ doit correspondre si renseigné
        if ($recherche !== '') {
            $q = strtolower($recherche);
            $match =
                str_contains(strtolower($e['student_fullname'] ?? ''), $q) ||
                str_contains(strtolower($e['mail']             ?? ''), $q) ||
                str_contains(strtolower($e['filiere']          ?? ''), $q) ||
                str_contains(strtolower($e['entreprise']       ?? ''), $q);
            if (!$match)
                return false;
        }
        return true;
    }));
}
?>
<section class="flex flex-col grow relative m-8">
    <div>
        <!-- En-tête -->
        <div class="mb-8">
            <h1 class="text-3xl font-extrabold">Gestion des stages</h1>
            <p class="mt-1">Suivi et administration des stages étudiants · Promotion 2023–2024</p>
        </div>

        <!-- KPIs cliquables -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">

            <a href="?filtre=tous" class="block rounded-2xl p-5 border <?= $filtre === 'tous' ? 'border-blue-500 ring-2 ring-blue-200' : 'border-gray-200' ?> hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Total étudiants</span>
                    <span class="bg-blue-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                    </span>
                </div>
                <div class="text-4xl font-extrabold text-gray-900"><?= $total ?></div>
                <div class="mt-1 text-xs">Tous les étudiants</div>
            </a>

            <a href="?filtre=sans_stage" class="block rounded-2xl p-5 border <?= $filtre === 'sans_stage' ? 'border-red-500 ring-2 ring-red-200' : 'border-gray-200' ?> hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Sans stage</span>
                    <span class="bg-red-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                    </span>
                </div>
                <div class="text-4xl font-extrabold text-red-600"><?= count($sans_stage) ?></div>
                <div class="mt-1 text-xs"><?= round(count($sans_stage) / $total * 100) ?>% du total</div>
            </a>

            <a href="?filtre=sans_tuteur" class="block rounded-2xl p-5 border <?= $filtre === 'sans_tuteur' ? 'border-yellow-500 ring-2 ring-yellow-200' : 'border-gray-200' ?> hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Sans tuteur</span>
                    <span class="bg-yellow-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    </span>
                </div>
                <div class="text-4xl font-extrabold text-yellow-600"><?= count($sans_tuteur) ?></div>
                <div class="mt-1 text-xs"><?= round(count($sans_tuteur) / $total * 100) ?>% du total</div>
            </a>

            <a href="?filtre=complet" class="block rounded-2xl p-5 border <?= $filtre === 'complet' ? 'border-green-500 ring-2 ring-green-200' : 'border-gray-200' ?> hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Stage complet</span>
                    <span class="bg-green-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    </span>
                </div>
                <div class="text-4xl font-extrabold text-green-600"><?= count($complets) ?></div>
                <div class="mt-1 text-xs"><?= round(count($complets) / $total * 100) ?>% du total</div>
            </a>

        </div>

        <!-- Barre d'outils -->
        <div class="bg-white border border-black/8 rounded-xl mb-5">
            <form method="GET">
                <input type="hidden" name="filtre" value="<?= $t->e($filtre) ?>">
                <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 p-3">

                    <!-- Recherche -->
                    <div class="relative flex-1 border border-black/8 rounded-lg py-2">
                        <?= $t->component("search_bar", props: [
                            "size" => "lg",
                            "value"=> $t->e($recherche),
                            "placeholder" => "Rechercher un étudiant, entreprise..."
                        ]) ?>
                    </div>

                    <!-- Filtre enseignant -->
                    <div class="relative">
                        <div class="absolute inset-y-0 left-3 flex items-center pointer-events-none">
                            <svg width="14" height="14" fill="none" viewBox="0 0 24 24">
                                <circle cx="12" cy="8" r="4" stroke="#94a3b8" stroke-width="1.8"/>
                                <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" stroke="#94a3b8" stroke-width="1.8" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <select name="id_enseignant"
                                class="text-sm text-[#0f2744] bg-slate-50 border border-black/8 rounded-lg pl-9 pr-8 py-2 outline-none focus:border-blue-500 focus:bg-white transition-colors appearance-none cursor-pointer min-w-44">
                            <option value="">Tous les enseignants</option>
                            <?php foreach ($enseignants as $ens): ?>
                                <option value="<?= $ens['id_enseignant'] ?>"
                                    <?= ($filtre_enseignant ?? '') == $ens['id_enseignant'] ? 'selected' : '' ?>>
                                    <?= htmlspecialchars($ens['nom'] . ' ' . $ens['prenom']) ?>
                                </option>
                            <?php endforeach; ?>
                        </select>
                        <div class="absolute inset-y-0 right-2.5 flex items-center pointer-events-none">
                            <svg width="12" height="12" fill="none" viewBox="0 0 24 24">
                                <polyline points="6 9 12 15 18 9" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                    </div>

                    <!-- Séparateur vertical -->
                    <div class="hidden sm:block w-px h-8 bg-black/8 shrink-0"></div>

                    <!-- Bouton soumettre -->
                    <button type="submit"
                            class="inline-flex items-center justify-center gap-2 px-4 py-2 bg-[#0f2744] hover:bg-[#1a3a5c] text-white text-sm font-medium rounded-lg transition-colors shrink-0">
                        <svg width="13" height="13" fill="none" viewBox="0 0 24 24">
                            <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
                            <line x1="21" y1="21" x2="16.65" y2="16.65" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                        Filtrer
                    </button>

                    <!-- Réinitialiser -->
                    <?php if ($filtre !== 'tous' || !empty($recherche) || !empty($filtre_enseignant)): ?>
                        <a href="?filtre=tous"
                        class="inline-flex items-center justify-center gap-1.5 px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 text-sm font-medium rounded-lg transition-colors shrink-0">
                            <svg width="13" height="13" fill="none" viewBox="0 0 24 24">
                                <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                            Réinitialiser
                        </a>
                    <?php endif; ?>

                </div>

                <!-- Bande inférieure : résultats + filtres actifs -->
                <?php $hasFilters = !empty($recherche) || !empty($filtre_enseignant) || $filtre !== 'tous'; ?>
                <?php if ($hasFilters): ?>
                    <div class="flex items-center gap-2 px-3 pb-3 flex-wrap">
                        <span class="text-xs text-slate-400">Filtres actifs :</span>

                        <?php if (!empty($recherche)): ?>
                            <span class="inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 bg-blue-50 text-blue-700 rounded-full">
                                "<?= $t->e($recherche) ?>"
                            </span>
                        <?php endif; ?>

                        <?php if (!empty($filtre_enseignant)): ?>
                            <?php $nomEns = ''; foreach ($enseignants as $e) { if ($e['id_enseignant'] == $filtre_enseignant) { $nomEns = $e['nom'] . ' ' . $e['prenom']; break; } } ?>
                            <span class="inline-flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 bg-purple-50 text-purple-700 rounded-full">
                                <?= htmlspecialchars($nomEns) ?>
                            </span>
                        <?php endif; ?>

                        <span class="ml-auto text-xs text-slate-400">
                            <?= count($liste) ?> résultat<?= count($liste) > 1 ? 's' : '' ?>
                        </span>
                    </div>
                <?php else: ?>
                    <div class="flex items-center justify-end px-3 pb-3">
                        <span class="text-xs text-slate-400">
                            <?= count($liste) ?> résultat<?= count($liste) > 1 ? 's' : '' ?>
                        </span>
                    </div>
                <?php endif; ?>

            </form>
        </div>

        <!-- Tableau -->
        <div class="rounded-2xl border overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-sm text-left">
                    <thead class="text-xs uppercase border-b bg-primary text-on-primary">
                        <tr>
                            <th class="px-6 py-4 font-semibold">Étudiant</th>
                            <th class="px-6 py-4 font-semibold">Programme</th>
                            <th class="px-6 py-4 font-semibold">Statut</th>
                            <th class="px-6 py-4 font-semibold">Entreprise</th>
                            <th class="px-6 py-4 font-semibold">Intitulé</th>
                            <th class="px-6 py-4 font-semibold">Période</th>
                            <th class="px-6 py-4 font-semibold">Tuteur</th>
                            <th class="px-6 py-4 font-semibold text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-500">
                        <?php if (empty($liste)): ?>
                        <tr>
                            <td colspan="7" class="px-6 py-16 text-center">
                                <div class="flex flex-col items-center gap-3 text-gray-500">
                                    <svg class="w-12 h-12" fill="none" stroke="currentColor" stroke-width="1" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                                    <p class="font-medium">Aucun étudiant trouvé</p>
                                </div>
                            </td>
                        </tr>
                        <?php else: foreach ($liste as $e):
                            $badgeClass = match($e['status']) {
                                'no-internship'  => 'bg-red-100 text-red-700',
                                'pending' => 'bg-yellow-100 text-yellow-700',
                                'completed'     => 'bg-green-100 text-green-700',
                                default       => '',
                            };
                            $badgeLabel = match($e['status']) {
                                'no-internship'  => 'Sans stage',
                                'pending' => 'Sans tuteur',
                                'completed'     => 'Complet',
                                default       => '',
                            };
                            $mots = explode(' ', $e['student_fullname']);
                            $initiales = implode('', array_map(fn($w) => strtoupper($w[0]), $mots));
                        ?>
                        <tr class="hover:bg-gray-100 transition">

                            <td class="px-6 py-4">
                                <div class="flex items-center gap-3">
                                    <div class="w-9 h-9 rounded-full bg-blue-100 flex items-center justify-center shrink-0">
                                        <span class="text-xs font-bold text-blue-600"><?= $t->e($initiales) ?></span>
                                    </div>
                                    <div>
                                        <div class="font-semibold text-gray-900"><?= $t->e($e['student_fullname']) ?></div>
                                        <div class="text-xs text-gray-500"><?= $t->e($e['mail']) ?></div>
                                    </div>
                                </div>
                            </td>

                            <td class="px-6 py-4 whitespace-nowrap text-gray-600"><?= $t->e($e['filiere']) ?></td>

                            <td class="px-6 py-4">
                                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold <?= $badgeClass ?>">
                                    <?= $badgeLabel ?>
                                </span>
                            </td>

                            <td class="px-6 py-4">
                                <?php if ($e['entreprise']): ?>
                                    <div class="font-medium text-gray-900"><?= $t->e($e['entreprise']) ?></div>
                                    <div class="text-xs text-gray-500"><?= $t->e($e['nature']) ?></div>
                                <?php else: ?>
                                    <span class="text-gray-400">—</span>
                                <?php endif; ?>
                            </td>

                            <td class="px-6 py-4">
                                <?php if ($e['entreprise']): ?>
                                    <div class="font-medium text-gray-900"><?= $t->e($e['intitulé']) ?></div>
                                    <div class="text-xs text-gray-500"><?= $t->e($e['nature']) ?></div>
                                <?php else: ?>
                                    <span class="text-gray-400">—</span>
                                <?php endif; ?>
                            </td>

                            <td class="px-6 py-4 whitespace-nowrap">
                                <?php if ($e['entreprise']): ?>
                                    <div class="text-gray-900"><?= date('d/m/Y', strtotime($e['date_debut'])) ?></div>
                                    <div class="text-xs text-gray-500">→ <?= date('d/m/Y', strtotime($e['date_fin'])) ?></div>
                                <?php else: ?>
                                    <span class="text-gray-400">—</span>
                                <?php endif; ?>
                            </td>

                            <td class="px-6 py-4">
                                <?php if ($e['teacher_fullname']): ?>
                                    <div class="font-medium text-gray-900"><?= $t->e($e['teacher_fullname']) ?></div>
                                    <div class="text-xs text-gray-500"><?= $t->e($e['teacher_mail']) ?></div>
                                <?php elseif ($e['entreprise']): ?>
                                    <span class="inline-flex items-center gap-1 text-xs text-yellow-600 font-medium">
                                        <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                                        À assigner
                                    </span>
                                <?php else: ?>
                                    <span class="text-gray-500">—</span>
                                <?php endif; ?>
                            </td>

                            <td class="px-6 py-4">
                                <div class="flex items-center justify-end gap-2">
                                    <?php if ($user['type'] === 'administratif'): ?>
                                        <?php if ($e['entreprise']): ?>
                                            <button
                                                data-modal-target="modal-<?= $e['id_etudiant'] ?>"
                                                data-modal-toggle="modal-<?= $e['id_etudiant'] ?>"
                                                class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-blue-700 bg-blue-50 rounded-lg hover:bg-blue-100 transition"
                                            >
                                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                                                Modifier
                                            </button>
                                        <?php else: ?>
                                            <a href="<?= $t->router->href('dashboard-create-stage', query: ['id_etudiant' => $e['id_etudiant']]) ?>"
                                                class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-green-700 bg-green-50 rounded-lg hover:bg-green-100 transition">
                                                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
                                                Ajouter stage
                                            </a>
                                        <?php endif; ?>
                                    <?php else: ?>
                                        <?php if ($e['entreprise']): ?>
                                            <form action="<?= $t->router->href("dashboard-stage-post") ?>" method="POST">
                                                <input type="hidden" name="id_stage" value="<?= $t->e($e['id_stage'] ?? '') ?>">
                                                <input type="hidden" name="entreprise" value="<?= $t->e($e['entreprise'] ?? '') ?>">
                                                <input type="hidden" name="intitulé" value="<?= $t->e($e['intitulé'] ?? '') ?>">
                                                <input type="hidden" name="nature" value="<?= $t->e($e['nature'] ?? '') ?>">
                                                <input type="hidden" name="date_debut" value="<?= $t->e($e['date_debut'] ?? '') ?>">
                                                <input type="hidden" name="date_fin" value="<?= $t->e($e['date_fin'] ?? '') ?>">
                                                <input type="hidden" name="description" value="<?= $t->e($e['description'] ?? '') ?>">
                                                <input type="hidden" name="adresse" value="<?= $t->e($e['adresse'] ?? '') ?>">
                                                <input type="hidden" name="code_postal" value="<?= $t->e($e['code_postal'] ?? '') ?>">
                                                <input type="hidden" name="ville" value="<?= $t->e($e['ville'] ?? '') ?>">
                                                <input type="hidden" name="pays" value="<?= $t->e($e['pays'] ?? '') ?>">
                                                <input type="hidden" name="id_enseignant" value="<?= $user['id'] === $e['id_enseignant'] ? '' : $t->e($user['id']) ?>">

                                                
                                                <button type="submit"
                                                    class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg hover:bg-blue-100 transition
                                                    <?= $user['id'] === $e['id_enseignant'] ? 'text-red-700 bg-red-50' : 'text-blue-700 bg-blue-50' ?>">
                                                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                                                    <?= $user['id'] === $e['id_enseignant'] ? 'Retirer' : 'Remplacer' ?> tuteur
                                                </button>
                                            </form>
                                        <?php endif; ?>
                                        <button
                                            data-modal-target="modal-<?= $e['id_etudiant'] ?>"
                                            data-modal-toggle="modal-<?= $e['id_etudiant'] ?>"
                                            class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-gray-700 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3.5 h-3.5">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                            </svg>
                                            Détail
                                        </button>
                                    <?php endif; ?>
                                </div>
                            </td>

                        </tr>
                        <?php endforeach; endif; ?>
                    </tbody>
                </table>
            </div>
        </div>

    </div>

    <!-- ===================== MODALS ===================== -->
    <?php foreach ($etudiants as $e):
        $isEdit = (bool)$e['entreprise'] && $user['type'] === 'administratif';
        $modalTitle = $isEdit ? 'Modifier le stage' : 'Détail du stage';
    ?>
    <div id="modal-<?= $e['id_etudiant'] ?>" tabindex="-1" aria-hidden="true"
        class="hidden overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 z-50 justify-center items-center w-full md:inset-0 h-[calc(100%-1rem)] max-h-full">
        <div class="relative p-4 w-full max-w-5xl max-h-full">
            <div class="relative bg-white rounded-2xl shadow">

                <!-- Header -->
                <div class="flex items-center justify-between p-6 border-b border-gray-200 bg-primary text-on-primary rounded-tl-2xl rounded-tr-2xl">
                    <div>
                        <h3 class="text-lg font-bold"><?= $modalTitle ?></h3>
                        <p class="text-sm mt-0.5"><?= $t->e($e['student_fullname']) ?> · <?= $t->e($e['filiere']) ?></p>
                    </div>
                    <button data-modal-hide="modal-<?= $e['id_etudiant'] ?>"
                        class="bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center">
                        <svg class="w-3 h-3" fill="none" viewBox="0 0 14 14"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/></svg>
                    </button>
                </div>

                <!-- Formulaire -->
                <form action="<?= $t->router->href("dashboard-stage-post") ?>" method="POST" class="p-6 space-y-5">
                    <input type="hidden" name="id_stage" value="<?= $t->e($e['id_stage'] ?? '') ?>">

                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div class="col-span-full">
                            <label class="block mb-2 text-sm font-medium text-gray-900">Entreprise <span class="text-red-500">*</span></label>
                            <input type="text" name="entreprise"
                                value="<?= $t->e($e['entreprise'] ?? '') ?>"
                                placeholder="Nom de l'entreprise"
                                required
                                <?= $isEdit ? '' : 'disabled' ?>
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"/>
                        </div>
                        <div>
                            <label class="block mb-2 text-sm font-medium text-gray-900">Intitulé <span class="text-red-500">*</span></label>
                            <input type="text" name="intitulé"
                                value="<?= $t->e($e['intitulé'] ?? '') ?>"
                                placeholder="Intitulé du poste"
                                required
                                <?= $isEdit ? '' : 'disabled' ?>
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"/>
                        </div>
                        <div>
                            <label class="block mb-2 text-sm font-medium text-gray-900">Nature <span class="text-red-500">*</span></label>
                            <input type="text" name="nature"
                                value="<?= $t->e($e['nature'] ?? '') ?>"
                                placeholder="Nature du poste"
                                required
                                <?= $isEdit ? '' : 'disabled' ?>
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"/>
                        </div>
                        <div>
                            <label class="block mb-2 text-sm font-medium text-gray-900">Date de début <span class="text-red-500">*</span></label>
                            <input type="date" name="date_debut"
                                value="<?= $t->e($e['date_debut'] ?? '') ?>"
                                required
                                <?= $isEdit ? '' : 'disabled' ?>
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"/>
                        </div>
                        <div>
                            <label class="block mb-2 text-sm font-medium text-gray-900">Date de fin <span class="text-red-500">*</span></label>
                            <input type="date" name="date_fin"
                                value="<?= $t->e($e['date_fin'] ?? '') ?>"
                                required
                                <?= $isEdit ? '' : 'disabled' ?>
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"/>
                        </div>
                        <div class="col-span-full">
                            <label class="block mb-2 text-sm font-medium text-gray-900">Description <span class="text-red-500">*</span></label>
                            <textarea name="description" id="" required <?= $isEdit ? '' : 'disabled' ?>
                                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"><?= $t->e($e['description'] ?? '') ?></textarea>
                        </div>
                    </div>

                    <div class="pt-2 border-t border-gray-100">
                        <p class="text-sm font-semibold text-gray-700 mb-4">
                            Adresse du stage
                            <?php if (!$isEdit): ?>
                                <span class="font-normal text-gray-500">(optionnel)</span>
                            <?php endif; ?>
                        </p>
                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <div class="col-span-full">
                                <label class="block mb-2 text-sm font-medium text-gray-900">Adresse</label>
                                <input type="text" name="adresse"
                                    value="<?= $t->e($e['adresse'] ?? '') ?>"
                                    placeholder="Adresse du stage"
                                    <?= $isEdit ? '' : 'disabled' ?>
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"/>
                            </div>
                            <div>
                                <label class="block mb-2 text-sm font-medium text-gray-900">Code postal</label>
                                <input type="text" name="code_postal"
                                    value="<?= $t->e($e['code_postal'] ?? '') ?>"
                                    placeholder="Code postal"
                                    <?= $isEdit ? '' : 'disabled' ?>
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"/>
                            </div>
                            <div>
                                <label class="block mb-2 text-sm font-medium text-gray-900">Ville <span class="text-red-500">*</span></label>
                                <input type="text" name="ville"
                                    value="<?= $t->e($e['ville'] ?? '') ?>"
                                    placeholder="Ville du stage"
                                    required
                                    <?= $isEdit ? '' : 'disabled' ?>
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"/>
                            </div>
                            <div>
                                <label class="block mb-2 text-sm font-medium text-gray-900">Pays</label>
                                <input type="text" name="pays"
                                    value="<?= $t->e($e['pays'] ?? '') ?>"
                                    placeholder="Pays du stage"
                                    <?= $isEdit ? '' : 'disabled' ?>
                                    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"/>
                            </div>
                        </div>
                    </div>

                    <!-- Tuteur -->
                    <div class="pt-2 border-t border-gray-100">
                        <p class="text-sm font-semibold text-gray-700 mb-4">
                            Tuteur entreprise
                            <?php if (!$isEdit): ?>
                                <span class="font-normal text-gray-500">(optionnel)</span>
                            <?php endif; ?>
                        </p>
                        <div class="grid grid-cols-1 gap-4">
                            <div>
                                <label class="block text-xs font-medium text-slate-600 mb-1.5" for="id_enseignant">Nom du tuteur</label>
                                <select id="id_enseignant" name="id_enseignant"
                                        <?= $isEdit ? '' : 'disabled' ?>
                                        class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors">
                                    <option value="">Aucun</option>
                                    <?php foreach ($enseignants as $ens): ?>
                                        <option value="<?= $ens['id_enseignant'] ?>"
                                            <?= ($e['id_enseignant'] ?? '') == $ens['id_enseignant'] ? 'selected' : '' ?>>
                                            <?= htmlspecialchars($ens['nom'] . ' ' . $ens['prenom']) ?>
                                        </option>
                                    <?php endforeach; ?>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Footer -->
                    <?php if ($user['type'] === 'administratif'): ?>
                        <div class="flex items-center justify-end gap-3 pt-4 border-t border-gray-100">
                            <button type="button" data-modal-hide="modal-<?= $e['id_etudiant'] ?>"
                                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition">
                                Annuler
                            </button>
                            <button type="submit"
                                class="px-4 py-2 text-sm font-medium text-white rounded-lg focus:ring-4 transition bg-blue-600 hover:bg-blue-700 focus:ring-blue-300">
                                Enregistrer
                            </button>
                        </div>
                    <?php endif; ?>

                </form>
            </div>
        </div>
    </div>
    <?php endforeach; ?>
</section>
<?php $t->endSlot(); ?>