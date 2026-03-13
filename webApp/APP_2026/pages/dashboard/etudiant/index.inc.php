<?php

    /////////////////
    // WARNING !!!!
    // Direct SQL queries are deprecated. Use backend API endpoints instead.
    /////////////////

    $id = $_SESSION['id'];

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
    $sql = "SELECT * FROM LNM_etudiant e WHERE e.id_etudiant LIKE $id;";
    $result = mysqli_query($conn, $sql);
    $student = mysqli_fetch_array($result);

    // Get polypoints info
    $polypoints = [];
    $sql = "SELECT * FROM ETU_polypoint WHERE id_etudiant=$id ORDER BY annee_universitaire DESC;";
    $result = mysqli_query($conn, $sql);
    while ($row = mysqli_fetch_assoc($result))
        $polypoints[] = $row;

    // Get stages info
    $stages = [];
    $sql="SELECT date_debut, date_fin, entreprise, nature FROM LNM_stage s WHERE s.id_etudiant=$id;";
    $result = mysqli_query($conn, $sql);
    while ($row = mysqli_fetch_assoc($result))
        $stages[] = $row;
?>

<section>
    <h1 class="text-3xl font-bold border-b pb-3">
        Page étudiante – <?= $student['nom'] ?> <?= $student['prenom'] ?>
    </h1>
    <p class="text-gray-500 mt-2">
        Tableau de suivi des polypoints et des stages
    </p>
</section>

<!-- POLYPOINTS -->
<section class="space-y-6">

    <h2 class="text-2xl font-semibold text-blue-700">
        Polypoints
    </h2>

    <!-- Résumé par année -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <? foreach (groupBy($polypoints, 'annee_universitaire') as $annee => $points) { ?>
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p class="font-semibold">Année <?= $annee ?></p>
                <p class="text-blue-900"><?= array_sum(array_column($points, 'nb_point'))?> polypoints enregistrés</p>
            </div>
        <? } ?>
    </div>

    <!-- Tableau des polypoints -->
    <div class="overflow-x-auto">
        <table class="w-full border border-gray-200 rounded-lg overflow-hidden shadow-sm bg-white">
            <thead class="bg-gray-100">
                <tr>
                    <th class="px-4 py-3 text-left">Action</th>
                    <th class="px-4 py-3 text-left">Détail</th>
                    <th class="px-4 py-3 text-center">Nombre</th>
                    <th class="px-4 py-3 text-left">Année</th>
                </tr>
            </thead>
            <tbody>
                <? foreach ($polypoints as $point) { ?>
                    <tr class="border-t hover:bg-gray-50">
                        <td class="px-4 py-3"><?= $point['intitule'] ?></td>
                        <td class="px-4 py-3"><?= $point['tache'] ?></td>
                        <td class="px-4 py-3 text-center font-semibold"><?= $point['nb_point'] ?></td>
                        <td class="px-4 py-3"><?= $point['annee_universitaire'] ?></td>
                    </tr>
                <? } ?>
            </tbody>
        </table>
    </div>

</section>

<!-- STAGES -->
<section class="space-y-6">

    <h2 class="text-2xl font-semibold text-green-700">
        Stages
    </h2>

    <!-- Tableau des stages -->
    <div class="overflow-x-auto">
        <table class="w-full border border-gray-200 rounded-lg overflow-hidden shadow-sm bg-white">
            <thead class="bg-gray-100">
                <tr>
                    <th class="px-4 py-3 text-left">Dates</th>
                    <th class="px-4 py-3 text-left">Entreprise</th>
                    <th class="px-4 py-3 text-left">Nature</th>
                </tr>
            </thead>
            <tbody>
                <? foreach ($stages as $stage) { ?>
                    <tr class="border-t hover:bg-gray-50">
                        <td class="px-4 py-3"><?= DateTime::createFromFormat('Y-m-d', $stage['date_debut'])->format('d/m/Y') ?> – <?= DateTime::createFromFormat('Y-m-d', $stage['date_fin'])->format('d/m/Y') ?></td>
                        <td class="px-4 py-3"><?= $stage['entreprise'] ?></td>
                        <td class="px-4 py-3"><?= $stage['nature'] ?></td>
                    </tr>
                <? } ?>
            </tbody>
        </table>
    </div>

</section>