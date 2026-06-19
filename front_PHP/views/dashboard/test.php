<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Test — Learnagement<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>
    <section class="flex-1 grow-1 justify-items-center">
        <div class="page-title">Polytech — UI Components Test</div>
        <div class="page-sub">Test de tous les composants dynamiques PHP.</div>
        <div class="test-section">
            <h3>0. Alerts</h3>
            <div class="col" style="max-width:520px; gap: 16px;">
                <?= $t->component("alert", props: [
                    "type" => "info",
                    "message" => "La période d'inscription se termine le 30 juin 2025."
                ]) ?>

                <?= $t->component("alert", props: [
                    "type" => "success",
                    "message" => "Votre dossier a bien été soumis."
                ]) ?>

                <?= $t->component("alert", props: [
                    "type" => "warning",
                    "message" => "Des pièces justificatives sont manquantes."
                ]) ?>

                <?= $t->component("alert", props: [
                    "type" => "error",
                    "message" => "Impossible de se connecter. Vérifiez vos identifiants."
                ]) ?>
            </div>
        </div>

        <div class="test-section">
            <h3>1. Controls (Checkboxes, Radios, Toggles)</h3>
            <div class="row" style="align-items:flex-start; gap:32px; flex-wrap:wrap;">
                <div class="col">
                    <?= $t->component("checkbox", props: ["label" => "Option A", "checked" => true]) ?>
                    <?= $t->component("checkbox", props: ["label" => "Option B"]) ?>
                    <?= $t->component("checkbox", props: ["label" => "Désactivé", "disabled" => true]) ?>
                </div>

                <div class="col">
                    <?= $t->component("radio", props: ["label" => "Étudiant", "name" => "demo-radio", "checked" => true]) ?>
                    <?= $t->component("radio", props: ["label" => "Enseignant", "name" => "demo-radio"]) ?>
                    <?= $t->component("radio", props: ["label" => "Administrateur", "name" => "demo-radio"]) ?>
                </div>

                <div class="col">
                    <?= $t->component("toggle", props: [
                        "label" => "Notifications",
                        "checked" => true,
                        "onchange" => "syncToggle(this)"
                    ]) ?>
                    <?= $t->component("toggle", props: [
                        "label" => "Mode sombre",
                        "onchange" => "syncToggle(this)"
                    ]) ?>
                    <?= $t->component("toggle", props: [
                        "label" => "Désactivé",
                        "disabled" => true
                    ]) ?>
                </div>
            </div>
        </div>

        <div class="test-section">
            <h3>2. Cards</h3>
            <div class="row" style="gap: 16px; align-items: flex-start;">
                <?= $t->component("card", props: [
                    "style" => "width:240px",
                    "header" =>
                        '<span class="card-title">Cours du semestre</span>' .
                        $t->component("badge", props: ["label" => "Actif", "color" => "success", "dot" => true]),
                    "body" => "Algorithmique avancée — 4 ECTS",
                    "footer" =>
                        $t->component("button", props: ["label" => "Voir", "variant" => "accent", "size" => "sm"]) .
                        $t->component("button", props: ["label" => "Ignorer", "variant" => "ghost", "size" => "sm"])
                ]) ?>

                <?= $t->component("card", props: [
                    "interactive" => true,
                    "style" => "width:240px",
                    "onclick" => "alert('Card clicked!')",
                    "header" =>
                        '<span class="card-title">Projet tuteuré</span>' .
                        $t->component("badge", props: ["label" => "En cours", "color" => "warning", "dot" => true]),
                    "body" => "Dépôt avant le 15 mai &middot; Groupe de 4",
                    "footer" => '<span style="font-size:12px; color:var(--c-text-3)">Cliquez pour détails &rarr;</span>'
                ]) ?>
            </div>
        </div>

        <div class="test-section">
            <h3>3. Buttons & Badges</h3>
            <div class="row">
                <?= $t->component("button", props: ["label" => "Small", "variant" => "primary", "size" => "sm"]) ?>
                <?= $t->component("button", props: ["label" => "Medium", "variant" => "primary"]) ?>
                <?= $t->component("button", props: ["label" => "Large", "variant" => "primary", "size" => "lg"]) ?>
            </div>
            <div class="row">
                <?= $t->component("badge", props: ["label" => "Primary", "color" => "primary"]) ?>
                <?= $t->component("badge", props: ["label" => "Accent", "color" => "accent"]) ?>
                <?= $t->component("badge", props: ["label" => "Neutre", "color" => "neutral"]) ?>
                <?= $t->component("badge", props: ["label" => "Actif", "color" => "success", "dot" => true]) ?>
                <?= $t->component("badge", props: ["label" => "En attente", "color" => "warning", "dot" => true]) ?>
                <?= $t->component("badge", props: ["label" => "Erreur", "color" => "error", "dot" => true]) ?>
            </div>
        </div>

        <div class="test-section">
            <h3>4. Avatars</h3>
            <div class="row">
                <?= $t->component("avatar", props: ["initials" => "JD", "size" => "sm", "color" => "primary"]) ?>
                <?= $t->component("avatar", props: ["initials" => "ML", "size" => "md"]) ?>
                <?= $t->component("avatar", props: ["initials" => "AP", "size" => "lg", "color" => "success"]) ?>

                <?php
                $groupData = [
                    ["initials" => "JD", "size" => "md", "color" => "primary"],
                    ["initials" => "ML", "size" => "md"],
                    ["initials" => "AP", "size" => "md", "color" => "success"],
                    ["initials" => "+4", "size" => "md", "color" => "warning", "tooltip" => "+4 autres"]
                ];
                ?>
                <?= $t->component("avatar_group", props: ["avatars" => $groupData]) ?>
            </div>
        </div>

        <div class="test-section">
            <h3>5. Dividers</h3>
            <div class="col" style="max-width:400px; gap:16px">
                <?= $t->component("divider") ?>
                <?= $t->component("divider", props: ["label" => "ou"]) ?>
                <?= $t->component("divider", props: ["label" => "Section suivante"]) ?>
            </div>
        </div>

        <div class="test-section">
            <h3>6. Inputs, Search & Select</h3>
            <div class="col" style="gap: 16px;">
                <?= $t->component("search_bar", props: ["id" => "search-demo"]) ?>
                <?= $t->component("search_bar", props: ["size" => "lg", "placeholder" => "Recherche globale…", "showClear" => false]) ?>

                <div class="row" style="align-items: flex-start;">
                    <div class="col" style="max-width:300px;">
                        <?= $t->component("input", props: [
                            "label" => "Nom complet",
                            "placeholder" => "ex. Marie Dupont",
                            "hint" => "Tel qu'il apparaît sur votre carte étudiant."
                        ]) ?>

                        <?= $t->component("input", props: [
                            "label" => "Email",
                            "type" => "email",
                            "value" => "invalide@",
                            "error" => true,
                            "errorMsg" => "Adresse email invalide."
                        ]) ?>
                    </div>

                    <div class="col" style="max-width:300px;">
                        <?= $t->component("input", props: [
                            "type" => "textarea",
                            "label" => "Description",
                            "placeholder" => "Décrivez votre projet…"
                        ]) ?>

                        <?= $t->component("select", props: [
                            "label" => "Département",
                            "minWidth" => 180,
                            "options" => ["Informatique", "Mécanique", "Électronique", "Génie civil"]
                        ]) ?>
                    </div>
                </div>
            </div>
        </div>

        <div class="test-section">
            <h3>7. Dropdown</h3>
            <?php
            $dropdownItems = [
                ["type" => "label", "label" => "Fichier"],
                ["label" => "Modifier", "icon" => "✎"],
                ["label" => "Dupliquer", "icon" => "⎘"],
                ["type" => "divider"],
                ["label" => "Supprimer", "icon" => "🗑", "danger" => true]
            ];
            ?>

            <?= $t->component("dropdown", props: [
                "id"    => "dd1",
                "label" => "Actions <span style='font-size:9px;opacity:.6'>▾</span>",
                "items" => $dropdownItems
            ]) ?>
            <?= $t->component("dropdown", props: [
                "id"    => "dd2",
                "label" => "Sélection <span style='font-size:9px;opacity:.6'>▾</span>",
                "items" => $dropdownItems
            ]) ?>
        </div>

        <div class="test-section">
            <h3>8. Skeletons</h3>
            <div class="row" style="align-items:flex-start; gap:24px">
                <div class="col" style="width:220px; gap:8px">
                    <?= $t->component("skeleton", props: ["type" => "title"]) ?>
                    <?= $t->component("skeleton", props: ["type" => "text"]) ?>
                    <?= $t->component("skeleton", props: ["type" => "text", "style" => "width:75%"]) ?>
                    <?= $t->component("skeleton", props: ["type" => "text", "style" => "width:55%"]) ?>
                </div>

                <div class="col" style="gap:8px">
                    <div class="row" style="gap:10px">
                        <?= $t->component("skeleton", props: ["type" => "avatar"]) ?>
                        <div class="col" style="gap:6px; width:160px">
                            <?= $t->component("skeleton", props: ["type" => "text", "style" => "width:120px; height:12px"]) ?>
                            <?= $t->component("skeleton", props: ["type" => "text", "style" => "width:80px; height:10px"]) ?>
                        </div>
                    </div>
                    <?= $t->component("skeleton", props: ["type" => "btn"]) ?>
                </div>
            </div>
        </div>

        <div class="test-section">
            <h3>9. Tabs</h3>
            <div class="col">
                <?= $t->component("tabs", props: [
                    "groupId" => "tabs-under",
                    "tabs" => [
                        ["label" => "Présentation", "active" => true],
                        ["label" => "Documents"],
                        ["label" => "Planning"],
                        ["label" => "Notes"]
                    ]
                ]) ?>

                <?= $t->component("tabs", props: [
                    "type" => "pill",
                    "groupId" => "tabs-pill",
                    "style" => "width:fit-content",
                    "tabs" => [
                        ["label" => "Semaine", "active" => true],
                        ["label" => "Mois"],
                        ["label" => "Année"]
                    ]
                ]) ?>
            </div>
        </div>
    </section>
<?php $t->endSlot(); ?>