<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Rendu — Learnagement<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>
<?php
    $token = $user["jwt_token"];
    $id = $user['id'];

    /////////////////
    // WARNING !!!!
    // Direct SQL queries are deprecated. Use backend API endpoints instead.
    /////////////////
    /*$rendus = [];
    $sql="SELECT r.date, r.description, p.parcour AS promo
    FROM LNM_rendu_module r 
        JOIN LNM_rendu_module_as_enseignant e ON r.id_rendu_module = e.id_rendu_module 
        JOIN LNM_rendu_module_as_etudiant retu ON retu.id_rendu_module = r.id_rendu_module
        JOIN LNM_etudiant etu ON etu.id_etudiant = retu.id_etudiant
        JOIN LNM_promo p ON p.id_promo = etu.id_promo
    WHERE e.id_enseignant = " . $_SESSION['id'] . "
        AND r.date >= NOW()
    ORDER BY date ASC";
    $result = mysqli_query($pdo, $sql);
    while ($row = mysqli_fetch_assoc($result))
        $rendus[] = $row;*/

    $rendus = get_rendus_enseignant($token, $id)
?>

<div class="p-4 space-y-8">
    <!-- Titre principal -->
    <h1 class="text-3xl font-bold text-gray-800 border-b pb-3">
        Enseignants
    </h1>

    <!-- Sous-titre -->
    <h2 class="text-2xl font-semibold text-blue-700">
        Liste des rendus vous concernant
    </h2>

    <?php if (empty($rendus)): ?>
        <p class='bg-green-50 border border-green-300 text-green-800 rounded-lg p-4'>
            🎉 Aucun rendu à venir pour le moment.
        </p>
    <?php else: ?>
        <?php foreach ($rendus as $rendu): ?>
            <div class='flex flex-col md:flex-row md:items-center md:justify-between
                    border rounded-lg p-4 hover:bg-gray-50 transition'>

                <div class='space-y-1'>
                    <p class='font-semibold text-gray-800'>
                        <?= $rendu['description'] ?>
                    </p>
                    <p class='text-sm text-gray-500'>
                        Promotion : <?= $rendu['promo'] ?>
                    </p>
                </div>

                <div class='mt-2 md:mt-0'>
                    <span class='inline-block bg-indigo-100 text-indigo-800
                                    px-3 py-1 rounded-full text-sm font-medium'>
                        À rendre le <?= htmlspecialchars($rendu['date']) ?> 
                    </span>
                </div>
            </div>
        <?php endforeach; ?>
    <?php endif; ?>
</div>

<?php $t->endSlot(); ?>