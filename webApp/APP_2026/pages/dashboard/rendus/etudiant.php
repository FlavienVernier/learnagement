<?php
    $rendus = [];
    $sql = "SELECT re.id_rendu_module AS id, r.description AS description, r.date AS date FROM `LNM_rendu_module_as_etudiant` re
    JOIN LNM_rendu_module r ON r.id_rendu_module=re.id_rendu_module WHERE re.date_depot is NULL 
    ORDER BY date ASC";
    $result = mysqli_query($conn, $sql);
    while ($row = mysqli_fetch_assoc($result))
        $rendus[] = $row;
?>

<div class="p-4 space-y-8">
    <!-- Titre principal -->
    <h1 class="text-3xl font-bold text-gray-800 border-b pb-3">
        Étudiants
    </h1>

    <!-- Sous-titre -->
    <h2 class="text-2xl font-semibold text-blue-700">
        Devoirs à rendre
    </h2>

    <?php if (empty($rendus)): ?>
        <p class="text-gray-600">
            Aucun devoir à rendre pour le moment. Profitez-en pour vous détendre ou avancer sur vos autres projets !
        </p>
    <?php else: ?>
        <!-- Formulaire des rendus -->
        <form method="post" action="?page=accueil&section=rendus_etudiants"
              class="bg-white rounded-xl shadow p-6 space-y-4">
    
            <?php foreach ($rendus as $rendu): ?>
                <label class='flex items-start gap-3 p-3 border rounded-lg hover:bg-gray-50 cursor-pointer'>
                    <input
                        type='checkbox'
                        name='checkbox[]'
                        value='<?= $rendu['id'] ?>'
                        class='mt-1 h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500'
                    >
                    <div>
                        <p class='font-medium text-gray-800'>
                            <?= htmlspecialchars($rendu['description']) ?>
                        </p>
                        <p class='text-sm text-gray-500'>
                            À rendre avant le <?= htmlspecialchars($rendu['date']) ?>
                        </p>
                    </div>
                </label>
            <?php endforeach; ?>
    
            <!-- Bouton de validation -->
            <div class="pt-4">
                <button
                    type="submit"
                    class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg transition disabled:opacity-50"
                >
                    Valider les éléments finis
                </button>
            </div>
        </form>
    <?php endif; ?>
</div>
