<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Création de stage<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>

<?php
    /////////////////
    // WARNING !!!!
    // Direct SQL queries are deprecated. Use backend API endpoints instead.
    /////////////////

    $sql = "SELECT e.id_etudiant, e.nom, e.prenom FROM LNM_etudiant e;";
    $stmt = mysqli_prepare($pdo, $sql);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);
    $etudiants = mysqli_fetch_all($result, MYSQLI_ASSOC);
    usort($etudiants, function ($a, $b) {
        return strcmp($a['nom'], $b['nom']);
    });

    $sql = "SELECT e.id_enseignant, e.nom, e.prenom FROM LNM_enseignant e;";
    $stmt = mysqli_prepare($pdo, $sql);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);
    $enseignants = mysqli_fetch_all($result, MYSQLI_ASSOC);
    usort($enseignants, function ($a, $b) {
        return strcmp($a['nom'], $b['nom']);
    });

?>

<!-- En-tête -->
<div class="mb-8">
    <h1 class="text-2xl font-medium text-[#0f2744] mb-1">Nouveau stage</h1>
    <p class="text-sm text-slate-500">Renseigner les informations du stage pour l'étudiant</p>
</div>

<form method="POST" action="<?= $t->router->href('dashboard-create-stage-post') ?>">

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Colonne principale -->
        <div class="lg:col-span-2 space-y-5">

            <!-- Entreprise -->
            <div class="bg-white border border-black/8 rounded-xl p-5">
                <h2 class="text-sm font-medium text-[#0f2744] mb-4 flex items-center gap-2">
                    <div class="w-6 h-6 rounded-md bg-blue-50 flex items-center justify-center">
                        <svg width="13" height="13" fill="none" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="#1b6ca8" stroke-width="1.8"/><polyline points="9 22 9 12 15 12 15 22" stroke="#1b6ca8" stroke-width="1.8"/></svg>
                    </div>
                    Entreprise
                </h2>

                <div class="space-y-4">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div class="sm:col-span-2">
                            <label class="block text-xs font-medium text-slate-600 mb-1.5" for="entreprise">
                                Nom de l'entreprise <span class="text-red-500">*</span>
                            </label>
                            <input type="text" id="entreprise" name="entreprise" required
                                   maxlength="100"
                                   placeholder="ex : Schneider Electric"
                                   value="<?= htmlspecialchars($_GET['entreprise'] ?? '') ?>"
                                   class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors placeholder-slate-400">
                        </div>

                        <div>
                            <label class="block text-xs font-medium text-slate-600 mb-1.5" for="intitule">
                                Intitulé du poste <span class="text-red-500">*</span>
                            </label>
                            <input type="text" id="intitule" name="intitule" required
                                   maxlength="50"
                                   placeholder="ex : Développeur back-end"
                                   value="<?= htmlspecialchars($_GET['intitule'] ?? '') ?>"
                                   class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors placeholder-slate-400">
                        </div>

                        <div>
                            <label class="block text-xs font-medium text-slate-600 mb-1.5" for="nature">
                                Nature du stage <span class="text-red-500">*</span>
                            </label>
                            <input type="text" id="nature" name="nature" required
                                    maxlength="150"
                                    placeholder="ex : Création d'un site web"
                                    value="<?= htmlspecialchars($_GET['nature'] ?? '') ?>"
                                    class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors placeholder-slate-400">
                        </div>
                    </div>

                    <div>
                        <label class="block text-xs font-medium text-slate-600 mb-1.5" for="description">
                            Description <span class="text-red-500">*</span>
                        </label>
                        <textarea id="description" name="description" required rows="4"
                                  placeholder="Décrire les missions, le contexte et les objectifs du stage..."
                                  class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors placeholder-slate-400 resize-none"
                        ><?= htmlspecialchars($_GET['description'] ?? '') ?></textarea>
                    </div>
                </div>
            </div>

            <!-- Adresse -->
            <div class="bg-white border border-black/8 rounded-xl p-5">
                <h2 class="text-sm font-medium text-[#0f2744] mb-4 flex items-center gap-2">
                    <div class="w-6 h-6 rounded-md bg-amber-50 flex items-center justify-center">
                        <svg width="13" height="13" fill="none" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" stroke="#d97706" stroke-width="1.8"/><circle cx="12" cy="10" r="3" stroke="#d97706" stroke-width="1.8"/></svg>
                    </div>
                    Localisation
                    <span class="text-xs font-normal text-slate-400">(optionnel)</span>
                </h2>

                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-medium text-slate-600 mb-1.5" for="adresse">Adresse</label>
                        <input type="text" id="adresse" name="adresse"
                               maxlength="190"
                               placeholder="ex : 35 rue Joseph Monier"
                               value="<?= htmlspecialchars($_GET['adresse'] ?? '') ?>"
                               class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors placeholder-slate-400">
                    </div>

                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div>
                            <label class="block text-xs font-medium text-slate-600 mb-1.5" for="code_GETal">Code postal</label>
                            <input type="text" id="code_GETal" name="code_GETal"
                                   maxlength="10"
                                   placeholder="ex : 92500"
                                   value="<?= htmlspecialchars($_GET['code_GETal'] ?? '') ?>"
                                   class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors placeholder-slate-400">
                        </div>

                        <div>
                            <label class="block text-xs font-medium text-slate-600 mb-1.5" for="ville">Ville <span class="text-red-500">*</span></label>
                            <input type="text" id="ville" name="ville" required
                                   maxlength="38"
                                   placeholder="ex : Rueil-Malmaison"
                                   value="<?= htmlspecialchars($_GET['ville'] ?? '') ?>"
                                   class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors placeholder-slate-400">
                        </div>

                        <div>
                            <label class="block text-xs font-medium text-slate-600 mb-1.5" for="pays">Pays</label>
                            <input type="text" id="pays" name="pays"
                                   maxlength="38"
                                   placeholder="ex : France"
                                   value="<?= htmlspecialchars($_GET['pays'] ?? 'France') ?>"
                                   class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors placeholder-slate-400">
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <!-- Colonne latérale -->
        <div class="space-y-5">

            <!-- Dates -->
            <div class="bg-white border border-black/8 rounded-xl p-5">
                <h2 class="text-sm font-medium text-[#0f2744] mb-4 flex items-center gap-2">
                    <div class="w-6 h-6 rounded-md bg-green-50 flex items-center justify-center">
                        <svg width="13" height="13" fill="none" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" stroke="#16a34a" stroke-width="1.8"/><line x1="3" y1="10" x2="21" y2="10" stroke="#16a34a" stroke-width="1.8"/><line x1="8" y1="2" x2="8" y2="6" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round"/><line x1="16" y1="2" x2="16" y2="6" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round"/></svg>
                    </div>
                    Période
                </h2>

                <div class="space-y-3">
                    <div>
                        <label class="block text-xs font-medium text-slate-600 mb-1.5" for="date_debut">
                            Date de début <span class="text-red-500">*</span>
                        </label>
                        <input type="date" id="date_debut" name="date_debut" required
                               value="<?= htmlspecialchars($_GET['date_debut'] ?? '') ?>"
                               class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors">
                    </div>

                    <div>
                        <label class="block text-xs font-medium text-slate-600 mb-1.5" for="date_fin">
                            Date de fin <span class="text-red-500">*</span>
                        </label>
                        <input type="date" id="date_fin" name="date_fin" required
                               value="<?= htmlspecialchars($_GET['date_fin'] ?? '') ?>"
                               class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors">
                    </div>

                    <!-- Indicateur durée -->
                    <div id="duree-indicator" class="hidden bg-green-50 border border-green-100 rounded-lg px-3 py-2 text-center">
                        <p class="text-xs text-green-700" id="duree-label">—</p>
                    </div>
                </div>
            </div>

            <!-- Encadrant -->
            <div class="bg-white border border-black/8 rounded-xl p-5">
                <h2 class="text-sm font-medium text-[#0f2744] mb-4 flex items-center gap-2">
                    <div class="w-6 h-6 rounded-md bg-purple-50 flex items-center justify-center">
                        <svg width="13" height="13" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4" stroke="#9333ea" stroke-width="1.8"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" stroke="#9333ea" stroke-width="1.8" stroke-linecap="round"/></svg>
                    </div>
                    Encadrant Polytech
                    <span class="text-xs font-normal text-slate-400">(optionnel)</span>
                </h2>

                <div>
                    <label class="block text-xs font-medium text-slate-600 mb-1.5" for="id_enseignant">Enseignant référent</label>
                    <select id="id_enseignant" name="id_enseignant"
                            class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors">
                        <option value="">Aucun</option>
                        <?php foreach ($enseignants as $ens): ?>
                            <option value="<?= $ens['id_enseignant'] ?>"
                                <?= ($_GET['id_enseignant'] ?? '') == $ens['id_enseignant'] ? 'selected' : '' ?>>
                                <?= htmlspecialchars($ens['nom'] . ' ' . $ens['prenom']) ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </div>

            <!-- Étudiant -->
            <div class="bg-white border border-black/8 rounded-xl p-5">
                <h2 class="text-sm font-medium text-[#0f2744] mb-4 flex items-center gap-2">
                    <div class="w-6 h-6 rounded-md bg-blue-50 flex items-center justify-center">
                        <svg width="13" height="13" fill="none" viewBox="0 0 24 24"><path d="M22 10v6M2 10l10-5 10 5-10 5z" stroke="#1b6ca8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M6 12v5c3 3 9 3 12 0v-5" stroke="#1b6ca8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                    Étudiant
                </h2>

                <div>
                    <label class="block text-xs font-medium text-slate-600 mb-1.5" for="id_etudiant">
                        Étudiant concerné <span class="text-red-500">*</span>
                    </label>
                    <select id="id_etudiant" name="id_etudiant" required
                            class="w-full text-sm text-[#0f2744] bg-slate-50 border border-black/10 rounded-lg px-3 py-2.5 outline-none focus:border-blue-500 focus:bg-white transition-colors">
                        <option value="" disabled <?= empty($_GET['id_etudiant']) ? 'selected' : '' ?>>Sélectionner...</option>
                        <?php foreach ($etudiants as $etu): ?>
                            <option value="<?= $etu['id_etudiant'] ?>"
                                <?= ($_GET['id_etudiant'] ?? '') == $etu['id_etudiant'] ? 'selected' : '' ?>>
                                <?= htmlspecialchars($etu['nom'] . ' ' . $etu['prenom']) ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>
            </div>

            <!-- Actions -->
            <div class="flex flex-col gap-2">
                <button type="submit"
                        class="w-full bg-[#0f2744] hover:bg-[#1a3a5c] text-white text-sm font-medium px-4 py-2.5 rounded-xl transition-colors flex items-center justify-center gap-2">
                    <svg width="14" height="14" fill="none" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    Créer le stage
                </button>
                <a href="<?= $t->router->href('dashboard-stage') ?>"
                   class="w-full text-center text-sm text-slate-500 hover:text-slate-700 bg-slate-100 hover:bg-slate-200 px-4 py-2.5 rounded-xl transition-colors">
                    Annuler
                </a>
            </div>

        </div>
    </div>

</form>

<script>
    const debut = document.getElementById('date_debut');
    const fin   = document.getElementById('date_fin');
    const box   = document.getElementById('duree-indicator');
    const label = document.getElementById('duree-label');

    function updateDuree() {
        if (!debut.value || !fin.value) { box.classList.add('hidden'); return; }
        const d1 = new Date(debut.value), d2 = new Date(fin.value);
        const jours = Math.round((d2 - d1) / 86400000);
        if (jours <= 0) { box.classList.add('hidden'); return; }
        const semaines = Math.floor(jours / 7);
        box.classList.remove('hidden');
        label.textContent = semaines > 0
            ? `Durée : ${semaines} semaine${semaines > 1 ? 's' : ''} et ${jours % 7} jour${jours % 7 > 1 ? 's' : ''} (${jours} jours)`
            : `Durée : ${jours} jour${jours > 1 ? 's' : ''}`;
    }

    debut.addEventListener('change', updateDuree);
    fin.addEventListener('change', updateDuree);
</script>
<?php $t->endSlot(); ?>