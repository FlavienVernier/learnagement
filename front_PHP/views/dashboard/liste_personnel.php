<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Liste du Personnel — Learnagement<?php $t->endSlot(); ?>

<?= $t->startSlot('stylesheet') ?>
    <style>
        <?= $t->stylesheet("dashboard/@stylesheet/liste_personnel") ?>
    </style>
<?php $t->endSlot(); ?>

<?= $t->startSlot('script.bottom') ?>
    <script>
        <?= $t->script("liste_personnel") ?>
    </script>
<?php $t->endSlot(); ?>

<?php
    $token = $user["jwt_token"];
    $list = $_GET['list'] ?? null;

    if ($list === 'prof') {
        // récupération via API
        $rows = get_enseignants($token);
        if (isset($_POST["query"]) && !empty($_POST["query"])) {
            $query = strtolower($_POST["query"]);
            $rows = array_filter($rows, function($row) use ($query) {
                return strpos(strtolower($row["mail"]), $query) !== false;
            });
        }
    } elseif ($list === 'etu') {
        // récupération via API
        $url = get_python_backend_url("etudiants/");
        $rows = get_endpoint($url, $token);
    }
?>

<?php $t->startSlot('content'); ?>
    <?php if (!empty($list)) : ?>
        <?php if ($list == 'prof') : ?>
            <form method='post' action='?list=prof'>
                <input type='text' name='query' placeholder='Entrez une recherche'>*
                <input class='bouton' type='submit' name='bouton_recherche' value='Rechercher'>
                <a href='<?= $t->router->href('dashboard-annuaire') ?>' class='bouton'>Retour</a>
            </form>
        <?php elseif ($list == 'etu') : ?>
            <form method='post' action='?list=etu'>
                <label id='formulaire'>Rechercher un étudiant :</label>
                <div id='conteneur_recherche'>
                    <div id='barre_recherche'>
                        <input type='text' id='search_input' placeholder='ex : Dupont'>
                        <button type='button' id='btn_recherche' class='bouton'>Rechercher</button>
                        <a href='<?= $t->router->href('dashboard-annuaire') ?>' class='bouton'>Retour</a>
                    </div>
                </div>
            </form>
        <?php else : ?>
            <p id='erreur_recherche'>Il n'y a pas de catégorie correspondant à la recherche.</p>
        <?php endif; ?>

        <?php if (!empty($rows)) : ?>
            <div class='conteneur_grid'>
                <div id='<?= $list == 'prof' ? 'enseignants' : 'etudiants' ?>'>
                    <?php foreach ($rows as $row) : ?>
                        <div class='<?= $list == 'prof' ? 'enseignant' : 'etudiant' ?>'>
                            <div id='<?= $list == 'prof' ? 'info_prof' : 'info_etu' ?>'>
                                <?= $row['nom'] . " " . $row['prenom'] ?>
                            </div>
                            <?php if ($list == 'prof') : ?>
                                <a id='mail_prof' href='mailto:<?= $row['mail'] ?>'>
                                    <?= $row['mail'] ?>
                                </a>
                            <?php else: ?>
                                <a id='mail_etu' href='mailto:<?= $row['mail'] ?>'>
                                    <?= $row['mail'] ?>
                                </a>
                                <p id='annee_filiere'>
                                    <?= $row['promo'] ?>
                                </p>
                            <?php endif; ?>
                            <div id='<?= $list == 'prof' ? 'photo_prof' : 'photo_etu' ?>'>
                                <img src='<?= $list == 'prof' ? $t->e(getenv("PERS_TROMBI_DIR")) : $t->e(getenv("ETU_TROMBI_DIR"))?><?= strtolower($row['nom']) . "_" . strtolower($row['prenom']) . ".jpg" ?>'
                                     onerror="this.src='<?= $t->e(getenv("DEFAULT_TROMBI_PICTURE"))?>'; this.onerror=null;"
                                     alt='<?= $list == 'prof' ? $t->e(getenv("PERS_TROMBI_DIR")) : $t->e(getenv("ETU_TROMBI_DIR"))?><?= strtolower($row['nom']) . "_" . strtolower($row['prenom']) . ".jpg or default image not found" ?>'>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>
            </div>
        <?php else : ?>
            <p id='erreur_recherche'>Il n'y a pas de résultat correspondant à la recherche.</p>
        <?php endif; ?>

        <div id='pagination'>
            <button id='btn_prev' class='bouton'>Précédent</button>
            <span id='page_info'></span>
            <button id='btn_next' class='bouton'>Suivant</button>
        </div>

    <?php else : ?>
        <div id='choix_liste'>
            <label id='formulaire'>Sélectionnez la liste à afficher</label>
            <div class='choice-container'>
                <a href='?list=prof' class='choice-card'>
                    <span>Enseignants</span>
                </a>
                <a href='?list=etu' class='choice-card'>
                    <span>Etudiants</span>
                </a>
            </div>
        </div>
    <?php endif; ?>
<?php $t->endSlot(); ?>