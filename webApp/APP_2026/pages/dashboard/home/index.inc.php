<link rel="stylesheet" href="./pages/dashboard/home/agenda.css" />
<script type="module" src="./pages/dashboard/home/agenda.js" defer></script>

<div class="max-w-7xl mx-auto p-8 space-y-12">
    <section class="space-y-2">
        <h1 class="text-4xl font-bold">
            Bienvenue sur l’intranet
        </h1>
        <p class="text-gray-500">
            Accès rapide à vos informations universitaires
        </p>
    </section>

    <section class="grid grid-cols-1 md:grid-cols-3 gap-6">

        <a href="<?= router("home", ["section" => "rendus"]) ?>" class="bg-white rounded-xl shadow p-6 hover:shadow-md transition space-y-2">
            <h2 class="text-xl font-semibold text-blue-700">
                📄 Rendus à venir
            </h2>
            <p class="text-gray-600">
                Consultez vos devoirs à rendre et leurs échéances.
            </p>
        </a>

        <? if ($_SESSION['type'] === 'etudiant') : ?>
            <a href="<?= router("home", ["section" => "etudiant"]) ?>"
            class="bg-white rounded-xl shadow p-6 hover:shadow-md transition space-y-2">
                <h2 class="text-xl font-semibold text-green-700">
                    ⭐ Polypoints
                </h2>
                <p class="text-gray-600">
                    Suivez vos engagements et points acquis.
                </p>
            </a>
        <? endif; ?>

        <a href="<?= router("home", ["section" => "ressources"]) ?>"
           class="bg-white rounded-xl shadow p-6 hover:shadow-md transition space-y-2">
            <h2 class="text-xl font-semibold text-purple-700">
                📚 Ressources
            </h2>
            <p class="text-gray-600">
                Accédez aux services et outils universitaires.
            </p>
        </a>

    </section>

    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-white rounded-xl shadow p-6 space-y-4">

            <div class="flex items-center justify-between">
                <h2 class="text-2xl font-semibold text-indigo-700">
                    📅 Agenda
                </h2>
            </div>

            <!-- Emplacement agenda -->
            <div id="calendar-container" class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center text-gray-500">
                <button id="prev-week">Semaine Précédente</button>
                <div id="current-month"></div>
                <button id="next-week">Semaine Suivante</button>

                <div id="calendar-wrapper">
                    <div id="time-scale"></div>
                    <!-- JS will generate all day columns and events here -->
                </div>

                <div id="tooltip"></div>
            </div>

        </div>

        <!-- ACTUALITÉS -->
        <div class="bg-white rounded-xl shadow p-6 space-y-4">

            <h2 class="text-2xl font-semibold text-orange-600">
                📰 Actualités
            </h2>

            <!-- Liste des actualités #idée -->
            <ul class="space-y-3">
                <li class="border-l-4 border-orange-400 pl-3">
                    <p class="font-medium">Ouverture des inscriptions sport</p>
                    <p class="text-sm text-gray-500">10 janvier 2025</p>
                </li>
                <li class="border-l-4 border-orange-400 pl-3">
                    <p class="font-medium">Fermeture exceptionnelle de la BU</p>
                    <p class="text-sm text-gray-500">18 janvier 2025</p>
                </li>
                <li class="border-l-4 border-orange-400 pl-3">
                    <p class="font-medium">Semaine de sensibilisation VSS</p>
                    <p class="text-sm text-gray-500">Du 22 au 26 janvier</p>
                </li>
            </ul>
        </div>
    </section>

</div>
