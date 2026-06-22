<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Gestion des Mobilités — Learnagement<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>
<section class="flex flex-col grow relative m-8 gap-6">
    <div>
        <div class="mb-8">
            <h1 class="text-3xl font-extrabold">Suivi des voeux de mobilité</h1>
            <p class="mt-1">Pilotage des dossiers mobilité internationale et universites partenaires</p>
        </div>

        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <article
                class="block rounded-2xl p-5 border border-gray-200 dark:border-gray-700 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Dossiers soumis</span>
                    <span class="bg-blue-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" stroke-width="2"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                    </span>
                </div>
                <div id="kpiStudents" class="text-4xl font-extrabold text-gray-900">0</div>
                <div class="mt-1 text-xs">Étudiants ayant validé leurs voeux</div>
            </article>

            <article
                class="block rounded-2xl p-5 border border-gray-200 dark:border-gray-700 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Dossiers incomplets</span>
                    <span class="bg-indigo-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" stroke-width="2"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                    </span>
                </div>
                <div id="kpiIncomplete" class="text-4xl font-extrabold text-indigo-600">0</div>
                <div class="mt-1 text-xs">Dossiers non encore soumis</div>
            </article>

            <article
                class="block rounded-2xl p-5 border border-gray-200 dark:border-gray-700 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Universites ciblées</span>
                    <span class="bg-green-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" stroke-width="2"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M3 5l9-3 9 3-9 3-9-3zm0 7l9 3 9-3m-18 7l9 3 9-3" />
                        </svg>
                    </span>
                </div>
                <div id="kpiUniversities" class="text-4xl font-extrabold text-green-600">0</div>
                <div class="mt-1 text-xs">Destinations distinctes demandées</div>
            </article>

            <article
                class="block rounded-2xl p-5 border border-gray-200 dark:border-gray-700 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Dépots récents</span>
                    <span class="bg-yellow-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" stroke-width="2"
                            viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </span>
                </div>
                <div id="kpiRecent" class="text-4xl font-extrabold text-yellow-600">0</div>
                <div class="mt-1 text-xs">Soumissions sur les 7 derniers jours</div>
            </article>
        </div>

        <div class="rounded-2xl border mb-6">
            <div class="p-4 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
                <div class="relative w-full lg:w-96">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </div>
                    <input id="wishesSearch" type="search" placeholder="Rechercher un etudiant, email ou universite..."
                        class="border text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5" />
                </div>
                <div class="flex flex-wrap items-center gap-3">
                    <label for="dossierStatusFilter"
                        class="text-xs font-semibold uppercase tracking-wide text-gray-500">Filtre dossier</label>
                    <select id="dossierStatusFilter" class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
                        <option value="tous">Tous</option>
                        <option value="complet">Complet</option>
                        <option value="incomplet">Incomplet</option>
                        <option value="recent">Recent (7 jours)</option>
                    </select>
                    <button id="resetDashboardFilters" type="button"
                        class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 transition">
                        Reinitialiser
                    </button>
                    <span id="wishesResultsCount" class="text-sm">0 resultat</span>
                </div>
            </div>
        </div>
        <div class="mb-4 flex flex-wrap gap-4">
            <button onclick="window.openProcedureModal()"
                class="inline-flex items-center gap-2 px-6 py-2.5 text-sm font-semibold text-white bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 hover:shadow transition">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Centre de Contrôle : Procédure
            </button>
            <button onclick="window.toggleDiagnostics()"
                class="inline-flex items-center gap-2 px-6 py-2.5 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 transition">
                <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" stroke-width="2"
                    viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
                </svg>
                Diagnostique & Statistiques
            </button>
        </div>

        <!-- Modal replaced the inline panel. The button is kept. -->

        <div class="rounded-2xl border overflow-hidden mb-8">
            <div class="overflow-x-auto">
                <table class="w-full text-sm text-left">
                    <thead class="text-xs uppercase border-b bg-primary text-on-primary">
                        <tr>
                            <th class="px-6 py-4 font-semibold">Etudiant</th>
                            <th class="px-6 py-4 font-semibold">Date soumission</th>
                            <th class="px-6 py-4 font-semibold">Statut</th>
                            <th class="px-6 py-4 font-semibold">Nombre de voeux</th>
                            <th class="px-6 py-4 font-semibold text-right">Details</th>
                        </tr>
                    </thead>
                    <tbody id="wishesTableBody" class="divide-y divide-gray-500">
                        <tr>
                            <td colspan="5" class="px-6 py-12 text-center text-gray-500">Chargement des dossiers...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div id="mapSection" class="relative rounded-2xl border overflow-hidden h-[36rem]">
        <div id="map" class="absolute inset-0" style="height: 100%; width: 100%;"></div>

        <div class="absolute top-[10px] left-[55px] z-[1000] flex max-w-[92vw] flex-col items-start gap-2.5">
            <div class="flex items-center gap-2">
                <button onclick="document.getElementById('filterForm').classList.toggle('hidden')"
                    class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow text-sm">
                    Filtres carte
                </button>
            </div>

            <form id="filterForm" onsubmit="return false;"
                class="hidden bg-white p-4 rounded-lg shadow-lg border border-gray-200">
                <div class="flex flex-wrap justify-center items-center gap-4">
                    <div class="flex flex-col">
                        <label for="semestreSelect" class="text-xs font-semibold text-gray-600 mb-1">Semestre</label>
                        <select name="semestre" id="semestreSelect" onchange="updateMap()"
                            class="border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary min-w-24">
                            <option value="Tous">Tous</option>
                            <option value="S8">S8</option>
                            <option value="S9">S9</option>
                        </select>
                    </div>
                    <div class="flex flex-col">
                        <label for="filiereSelect" class="text-xs font-semibold text-gray-600 mb-1">Filiere</label>
                        <select name="filiere" id="filiereSelect" onchange="updateMap()"
                            class="border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary min-w-48">
                            <option value="toutes">Toutes</option>
                        </select>
                    </div>
                    <div class="flex flex-col">
                        <div class="flex justify-between items-center mb-1">
                            <label for="noteMinRange" class="text-xs font-semibold text-gray-600">Note minimale</label>
                            <span id="noteMinValue" class="text-xs font-bold text-gray-700">20</span>
                        </div>
                        <input type="range" name="notemin" id="noteMinRange" min="0" max="20" value="20"
                            class="w-32 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary"
                            oninput="document.getElementById('noteMinValue').innerText = this.value; updateMap()">
                    </div>
                </div>
            </form>
        </div>
    </div>

    <div class="rounded-2xl border overflow-hidden">
        <div class="p-4 border-b flex flex-col lg:flex-row gap-3 lg:items-center lg:justify-between">
            <div>
                <h2 class="text-lg font-bold">Universités partenaires</h2>
                <p class="text-sm text-gray-500">Ajout et ajustement des places par filière/semestre.</p>
            </div>
            <div class="flex flex-wrap items-center gap-2">
                <input id="universityAdminSearch" type="search" placeholder="Rechercher une universite..."
                    class="border text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-64 p-2.5" />
                <button id="addUniversityRowBtn" type="button"
                    class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition">
                    Ajouter une universite
                </button>
            </div>
        </div>
        <div id="addUniversityPanel" class="hidden p-4 border-b bg-gray-50">
            <div class="mb-3 flex items-center justify-between">
                <h3 class="text-sm font-semibold text-gray-800">Nouvelle université partenaire</h3>
                <button id="cancelAddUniversityBtn" type="button"
                    class="text-xs px-3 py-1.5 rounded bg-gray-200 text-gray-700 hover:bg-gray-300">Annuler</button>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-3 mb-3">
                <input id="newUniName" type="text" placeholder="Nom de l'université *"
                    class="border rounded px-3 py-2 text-sm" />
                <input id="newUniCountry" type="text" placeholder="Pays *" class="border rounded px-3 py-2 text-sm" />
                <input id="newUniCode" type="text" placeholder="Code" class="border rounded px-3 py-2 text-sm" />
                <input id="newUniAddress" type="text" placeholder="Adresse"
                    class="border rounded px-3 py-2 text-sm lg:col-span-2" />
                <input id="newUniWebsite" type="url" placeholder="Site web" class="border rounded px-3 py-2 text-sm" />
                <input id="newUniLanguages" type="text" placeholder="Langues (ex: Anglais, Espagnol)"
                    class="border rounded px-3 py-2 text-sm lg:col-span-2" />
                <div class="grid grid-cols-3 gap-2 lg:col-span-1">
                    <input id="newUniLatitude" type="number" step="0.000001" placeholder="Latitude"
                        class="border rounded px-3 py-2 text-sm" />
                    <input id="newUniLongitude" type="number" step="0.000001" placeholder="Longitude"
                        class="border rounded px-3 py-2 text-sm" />
                    <input id="newUniNoteMin" type="number" step="0.01" min="0" max="20" placeholder="Note min"
                        class="border rounded px-3 py-2 text-sm" />
                </div>
                <select id="newUniType" class="border rounded px-3 py-2 text-sm">
                    <option value="ERASMUS">ERASMUS</option>
                    <option value="Bilateral">Bilateral</option>
                </select>
            </div>

            <div class="rounded border bg-white p-3">
                <div class="mb-2 flex items-center justify-between">
                    <h4 class="text-xs font-semibold uppercase tracking-wide text-gray-600">Places par filière /
                        semestre</h4>
                    <button id="addNewUniPlaceRowBtn" type="button"
                        class="text-xs px-2 py-1 rounded bg-gray-200 text-gray-700 hover:bg-gray-300">Ajouter une
                        ligne</button>
                </div>
                <div id="newUniPlacesRows" class="space-y-2"></div>
            </div>

            <div class="mt-3 flex items-center justify-end gap-2">
                <button id="saveNewUniversityBtn" type="button"
                    class="text-xs px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700">Créer
                    l'université</button>
            </div>
        </div>
        <div class="overflow-x-auto">
            <table class="w-full text-sm text-left">
                <thead class="text-xs uppercase border-b bg-primary text-on-primary">
                    <tr>
                        <th class="px-6 py-4 font-semibold">Universite</th>
                        <th class="px-6 py-4 font-semibold">Pays</th>
                        <th class="px-6 py-4 font-semibold">Code</th>
                        <th class="px-6 py-4 font-semibold">Demandes</th>
                        <th class="px-6 py-4 font-semibold text-right">Actions</th>
                    </tr>
                </thead>
                <tbody id="universitiesAdminBody" class="divide-y divide-gray-500">
                    <tr>
                        <td colspan="5" class="px-6 py-10 text-center text-gray-500">Chargement des universites...</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div id="streetViewModal" class="streetview-modal">
        <div class="streetview-content">
            <div class="streetview-header">
                <h2 id="streetViewTitle" class="text-lg font-semibold"></h2>
                <button class="streetview-close" onclick="window.closeStreetViewModal()">x</button>
            </div>
            <div id="streetViewPanoramaModal" style="width: 100%; height: 100%;"></div>
        </div>
    </div>

    <!-- Procedure Modal -->
    <div id="procedureModal"
        class="hidden fixed inset-0 bg-gray-900 bg-opacity-50 z-[2000] flex items-center justify-center">
        <div class="bg-white rounded-xl shadow-xl w-full max-w-[90vw] xl:max-w-7xl p-6 max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-start mb-6">
                <h3 class="text-xl font-bold text-gray-900 flex items-center gap-2">
                    <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" stroke-width="2"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    Centre de Contrôle : Mobilité
                </h3>
                <button onclick="document.getElementById('procedureModal').classList.add('hidden')"
                    class="text-gray-400 hover:text-gray-600">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                        </path>
                    </svg>
                </button>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-0">
                <!-- COLONNE 1 -->
                <div class="space-y-6 lg:border-r lg:border-gray-200 lg:pr-8">

                    <!-- ETAPE 1 -->
                    <div>
                        <h4
                            class="text-sm font-bold text-gray-800 uppercase tracking-wide mb-2 flex items-center gap-2">
                            <span class="bg-gray-200 text-gray-700 px-2 py-0.5 rounded text-xs">Étape 1</span>
                            Gestion des soumissions
                        </h4>

                        <!-- Annulation individuelle -->
                        <div class="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-100">
                            <h5 class="text-xs font-bold text-gray-700 mb-2">Annulation de soumission individuelle</h5>
                            <p class="text-[11px] text-gray-500 mb-3">Redonner la main à un étudiant pour modifier ses
                                choix avant la clôture finale.</p>
                            <select id="resetStudentSelect" onchange="window.onResetStudentChange()"
                                class="w-full text-sm border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 mb-3">
                                <option value="">Sélectionnez un étudiant...</option>
                            </select>
                            <div id="resetStudentDetails"
                                class="hidden bg-white p-3 rounded border text-xs text-gray-600 mb-3">
                                <p><strong>Nom complet:</strong> <span id="rsName"></span></p>
                                <p><strong>Email:</strong> <span id="rsEmail"></span></p>
                                <p><strong>Filière:</strong> <span id="rsFiliere"></span></p>
                            </div>
                            <button id="btnResetWishes" onclick="window.resetStudentWishes()"
                                class="hidden inline-flex items-center gap-2 px-3 py-1.5 text-xs font-semibold text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 transition">
                                <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                </svg>
                                Annuler la soumission
                            </button>
                        </div>

                        <h5 class="text-xs font-bold text-gray-700 mb-2">Clôture globale</h5>
                        <p class="text-xs text-gray-500 mb-3">Verrouille tous les dossiers pour figer les données et
                            force la soumission des vœux incomplets.</p>
                        <button onclick="window.forceSubmitWishesUI()"
                            class="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-red-600 rounded-lg hover:bg-red-700 transition">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                            </svg>
                            Clôturer les soumissions
                        </button>
                    </div>

                    <hr class="border-gray-200">

                    <!-- ETAPE 2 -->
                    <div>
                        <h4
                            class="text-sm font-bold text-gray-800 uppercase tracking-wide mb-2 flex items-center gap-2">
                            <span class="bg-gray-200 text-gray-700 px-2 py-0.5 rounded text-xs">Étape 2</span>
                            Exécution de l'algorithme
                        </h4>

                        <div class="p-4 bg-gray-50 rounded-lg border border-gray-100 mb-4">
                            <h5 class="text-xs font-bold text-gray-700 mb-2">Quotas de mobilité par filière et semestre
                            </h5>
                            <p class="text-[11px] text-gray-500 mb-3">Indiquez le nombre d'étudiants autorisés à partir
                                en mobilité pour chaque filière et par semestre.</p>

                            <div class="flex flex-wrap items-end gap-2 mb-4">
                                <div class="flex-1 min-w-[120px]">
                                    <label class="block text-[10px] font-bold text-gray-600 mb-1">Filière</label>
                                    <select id="quotaMobilityFiliere"
                                        class="w-full text-xs border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500">
                                        <option value="">Chargement...</option>
                                    </select>
                                </div>
                                <div class="w-24">
                                    <label class="block text-[10px] font-bold text-gray-600 mb-1">Semestre</label>
                                    <select id="quotaMobilitySemester"
                                        class="w-full text-xs border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500">
                                        <option value="8">S8</option>
                                        <option value="9">S9</option>
                                    </select>
                                </div>
                                <div class="w-24">
                                    <label class="block text-[10px] font-bold text-gray-600 mb-1">Places</label>
                                    <input type="number" id="quotaMobilityPlaces" min="0" value="0"
                                        class="w-full text-xs border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500">
                                </div>
                                <button onclick="window.addMobilityQuota()"
                                    class="px-3 py-1.5 text-xs font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded transition whitespace-nowrap"
                                    style="height: 34px;">
                                    Ajouter
                                </button>
                            </div>

                            <div id="mobilityQuotasList" class="flex flex-col gap-2 h-18 overflow-y-auto">
                                <!-- JS will populate this -->
                                <div id="mobilityQuotasEmpty" class="text-[11px] text-gray-400 italic">Aucun quota
                                    défini. L'algorithme n'affectera personne si les quotas sont vides.</div>
                            </div>
                        </div>

                        <div class="mt-4 flex items-center gap-4" id="assignmentActions">
                            <button onclick="window.runAssignmentUI()"
                                class="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                                </svg>
                                Lancer l'affectation automatique
                            </button>
                            <div id="quotaCounter"
                                class="text-xs font-semibold text-gray-600 bg-gray-100 px-3 py-1.5 rounded-full border border-gray-200 shadow-sm transition-colors duration-300">
                                0 / 0 quotas configurés
                            </div>
                        </div>

                        <!-- Progress UI -->
                        <div id="assignmentProgressContainer"
                            class="hidden mt-4 p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
                            <div class="flex justify-between text-xs font-semibold text-gray-700 mb-2">
                                <span id="assignmentProgressText">Démarrage...</span>
                                <span id="assignmentProgressPercent">0%</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2.5">
                                <div id="assignmentProgressBar"
                                    class="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                                    style="width: 0%"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- COLONNE 2 -->
                <div class="space-y-6 lg:pl-8">
                    <!-- ETAPE 3 -->
                    <div>
                        <h4
                            class="text-sm font-bold text-gray-800 uppercase tracking-wide mb-2 flex items-center gap-2">
                            <span class="bg-gray-200 text-gray-700 px-2 py-0.5 rounded text-xs">Étape 3</span>
                            Validation manuelle des affectations
                        </h4>
                        <p class="text-xs text-gray-500 mb-3">Modifiez manuellement le statut d'un étudiant s'il vous
                            confirme sa décision en personne.</p>



                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
                            <!-- Colonne de gauche : Modification -->
                            <div>
                                <div class="mb-4">
                                    <label for="validationStudentSelect"
                                        class="block text-xs font-semibold text-gray-700 mb-1">Sélectionnez un étudiant
                                        affecté :</label>
                                    <select id="validationStudentSelect" onchange="window.onValidationStudentChange()"
                                        class="w-full text-sm border-gray-300 rounded focus:ring-blue-500 focus:border-blue-500">
                                        <option value="">Chargement...</option>
                                    </select>
                                </div>

                                <div id="validationStudentDetails"
                                    class="hidden bg-gray-50 p-3 rounded border border-gray-200 mb-3 text-sm">
                                    <div class="grid grid-cols-2 gap-2 mb-3">
                                        <p><strong>Nom:</strong> <span id="vsNom"></span></p>
                                        <p><strong>Filière:</strong> <span id="vsFiliere"></span></p>
                                        <p class="col-span-2"><strong>Affectation:</strong> <span
                                                id="vsUniversity"></span></p>
                                        <p class="col-span-2 flex flex-wrap items-center gap-2">
                                            <strong>Statut:</strong>
                                            <span id="vsStatusBadge"
                                                class="px-2 py-0.5 rounded text-xs font-bold text-white"></span>
                                        </p>
                                    </div>

                                    <div class="flex flex-col xl:flex-row flex-wrap gap-2">
                                        <button id="btnForceAccept"
                                            onclick="window.updateAssignmentStatusUI('accepted')"
                                            class="flex-1 justify-center inline-flex items-center gap-1 px-3 py-1.5 text-xs font-semibold text-white bg-green-600 rounded hover:bg-green-700 transition">
                                            Forcer l'acceptation
                                        </button>
                                        <button id="btnForcePending"
                                            onclick="window.updateAssignmentStatusUI('pending')"
                                            class="flex-1 justify-center inline-flex items-center gap-1 px-3 py-1.5 text-xs font-semibold text-white bg-amber-600 rounded hover:bg-amber-700 transition">
                                            Remettre en attente
                                        </button>
                                        <button id="btnForceDecline"
                                            onclick="window.updateAssignmentStatusUI('declined')"
                                            class="flex-1 justify-center inline-flex items-center gap-1 px-3 py-1.5 text-xs font-semibold text-white bg-red-600 rounded hover:bg-red-700 transition">
                                            Forcer le refus
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <!-- Colonne de droite : Graphe et Export -->
                            <div
                                class="bg-gray-50 border rounded-xl p-4 shadow-sm flex flex-col items-center justify-center">
                                <h4 class="font-bold text-gray-700 mb-2 text-center text-sm">Statut des Affectations
                                </h4>
                                <div class="w-full relative h-40 flex justify-center">
                                    <canvas id="chartEtape3Status"></canvas>
                                </div>
                                <div
                                    class="mt-4 flex gap-3 text-[11px] font-semibold text-indigo-600 flex-wrap justify-center">
                                    <a href="#" onclick="exportAssignedData('accepted')"
                                        class="hover:underline flex items-center gap-1"><svg class="w-3 h-3" fill="none"
                                            stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-3 3m0 0l-3-3m3 3V4" />
                                        </svg> Acceptés</a>
                                    <a href="#" onclick="exportAssignedData('pending')"
                                        class="hover:underline flex items-center gap-1"><svg class="w-3 h-3" fill="none"
                                            stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-3 3m0 0l-3-3m3 3V4" />
                                        </svg> En attente</a>
                                    <a href="#" onclick="exportAssignedData('declined')"
                                        class="hover:underline flex items-center gap-1"><svg class="w-3 h-3" fill="none"
                                            stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-3 3m0 0l-3-3m3 3V4" />
                                        </svg> Refusés</a>
                                </div>
                            </div>
                        </div>

                        <!-- Bouton Cloture Phase d'acceptation deplace a la fin de l'etape 3 -->
                        <div class="mt-4 flex justify-center">
                            <button onclick="window.closeAssignmentPhase()"
                                class="px-4 py-2 bg-red-600 text-white rounded-lg shadow-sm text-sm font-bold hover:bg-red-700 transition">
                                Clôture de la phase d'acceptation
                            </button>
                        </div>
                    </div>

                    <hr class="border-gray-200">



                    <!-- ETAPE 4 -->
                    <div>
                        <h4
                            class="text-sm font-bold text-gray-800 uppercase tracking-wide mb-2 flex items-center gap-2">
                            <span class="bg-gray-200 text-gray-700 px-2 py-0.5 rounded text-xs">Étape 4</span>
                            Exportation des Résultats
                        </h4>
                        <p class="text-xs text-gray-500 mb-3">Téléchargez les listes finales pour communication aux
                            universités partenaires.</p>
                        <div class="flex gap-3">
                            <button onclick="exportWishes()"
                                class="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-green-700 bg-green-100 rounded-lg hover:bg-green-200 transition">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                </svg>
                                Vœux (XLSX)
                            </button>
                            <button onclick="exportAssignments()"
                                class="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-green-700 bg-green-100 rounded-lg hover:bg-green-200 transition">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                </svg>
                                Affectations (XLSX)
                            </button>
                            <button onclick="exportPlaces()"
                                class="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-green-700 bg-green-100 rounded-lg hover:bg-green-200 transition">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                </svg>
                                État des places (XLSX)
                            </button>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- Diagnostics Modal -->
    <div id="diagnosticsModal"
        class="hidden fixed inset-0 bg-gray-900 bg-opacity-50 z-[2000] flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-xl w-full max-w-5xl p-6 max-h-[95vh] overflow-y-auto">
            <div class="flex items-center justify-between mb-6">
                <h3 class="text-xl font-bold text-gray-900 flex items-center gap-2">
                    <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" stroke-width="2"
                        viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
                    </svg>
                    Diagnostique & Statistiques (Telling Story)
                </h3>
                <button onclick="document.getElementById('diagnosticsModal').classList.add('hidden')"
                    class="text-gray-400 hover:text-gray-600 transition">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Graphe 1 -->
                <div class="bg-gray-50 border rounded-xl p-4 shadow-sm flex flex-col items-center">
                    <h4 class="font-bold text-gray-700 mb-2 text-center text-sm">1. Statut Global de la Mobilité</h4>
                    <p class="text-xs text-gray-500 mb-4 text-center">La population totale de la promotion étudiée.</p>
                    <div class="w-full relative h-48 flex justify-center">
                        <canvas id="chartGlobalStatus"></canvas>
                    </div>
                    <div class="mt-4 flex gap-4 text-xs font-semibold text-indigo-600">
                        <a href="#" onclick="exportDiagnosticData('validated')"
                            class="hover:underline flex items-center gap-1"><svg class="w-3 h-3" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-3 3m0 0l-3-3m3 3V4" />
                            </svg> Validés</a>
                        <a href="#" onclick="exportDiagnosticData('remaining')"
                            class="hover:underline flex items-center gap-1"><svg class="w-3 h-3" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-3 3m0 0l-3-3m3 3V4" />
                            </svg> Non validés</a>
                    </div>
                </div>

                <!-- Graphe 2 -->
                <div class="bg-gray-50 border rounded-xl p-4 shadow-sm flex flex-col items-center">
                    <h4 class="font-bold text-gray-700 mb-2 text-center text-sm">2. Avancement des étudiants à traiter
                    </h4>
                    <p class="text-xs text-gray-500 mb-4 text-center">Ceux qui n'ont pas encore validé leur mobilité.
                    </p>
                    <div class="w-full relative h-48 flex justify-center">
                        <canvas id="chartWishesStatus"></canvas>
                    </div>
                    <div class="mt-4 flex gap-3 text-[11px] font-semibold text-indigo-600 flex-wrap justify-center">
                        <a href="#" onclick="exportDiagnosticData('submitted')"
                            class="hover:underline flex items-center gap-1"><svg class="w-3 h-3" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-3 3m0 0l-3-3m3 3V4" />
                            </svg> Soumis</a>
                        <a href="#" onclick="exportDiagnosticData('in_progress')"
                            class="hover:underline flex items-center gap-1"><svg class="w-3 h-3" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-3 3m0 0l-3-3m3 3V4" />
                            </svg> En cours</a>
                        <a href="#" onclick="exportDiagnosticData('retardataires')"
                            class="hover:underline flex items-center gap-1"><svg class="w-3 h-3" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-3 3m0 0l-3-3m3 3V4" />
                            </svg> Retardataires</a>
                    </div>
                </div>

                <!-- Graphe 3 -->
                <div class="bg-gray-50 border rounded-xl p-4 shadow-sm flex flex-col items-center">
                    <h4 class="font-bold text-gray-700 mb-2 text-center text-sm">3. Nombre de choix effectués</h4>
                    <p class="text-xs text-gray-500 mb-4 text-center">Répartition du nombre de vœux enregistrés.</p>
                    <div class="w-full relative h-48 flex justify-center">
                        <canvas id="chartWishesDistribution"></canvas>
                    </div>
                </div>
            </div>

            <div class="mt-8 flex justify-end">
                <button onclick="document.getElementById('diagnosticsModal').classList.add('hidden')"
                    class="px-5 py-2 text-sm font-semibold text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-lg transition">Fermer</button>
            </div>
        </div>
    </div>
    <!-- Confirmation Code Modal -->
    <div id="confirmActionModal"
        class="hidden fixed inset-0 bg-gray-900 bg-opacity-75 z-[3000] flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-xl w-full max-w-sm p-6 text-center">
            <h3 class="text-lg font-bold text-red-600 mb-2">Action Critique</h3>
            <p class="text-sm text-gray-600 mb-4" id="confirmActionDescription"></p>

            <div class="bg-gray-100 p-3 rounded mb-4 font-mono text-xl tracking-[0.2em] font-bold text-gray-800 select-none"
                id="confirmActionCodeDisplay"></div>

            <p class="text-xs text-gray-500 mb-2">Veuillez recopier le code ci-dessus pour confirmer :</p>
            <input type="text" id="confirmActionCodeInput"
                class="w-full text-center text-lg font-mono border-gray-300 rounded focus:ring-red-500 focus:border-red-500 mb-4 uppercase"
                placeholder="Entrez le code" autocomplete="off">

            <div class="flex gap-3 justify-center">
                <button onclick="document.getElementById('confirmActionModal').classList.add('hidden')"
                    class="px-4 py-2 text-sm font-semibold text-gray-600 bg-gray-200 hover:bg-gray-300 rounded transition">Annuler</button>
                <button id="confirmActionButton"
                    class="px-4 py-2 text-sm font-semibold text-white bg-red-600 hover:bg-red-700 rounded transition opacity-50 cursor-not-allowed"
                    disabled>Confirmer</button>
            </div>
        </div>
    </div>
</section>
<?php $t->endSlot(); ?>


<?php $t->startSlot('stylesheet'); ?>
<!-- Import Leaflet CSS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
<link rel="stylesheet" href="/theme/mobility-map.css" />
<?php $t->endSlot(); ?>


<?php $t->startSlot('script.top'); ?>
<?php
$googleMapsApiKey = getenv('GOOGLE_MAPS_API_KEY') ?: ($_ENV['GOOGLE_MAPS_API_KEY'] ?? '');
?>
<!-- Import Leaflet JS -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin="">
    </script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

<!-- Google Maps API pour Street View interactif -->
<script src="https://maps.googleapis.com/maps/api/js?key=<?= urlencode($googleMapsApiKey) ?>&libraries=places"></script>

<!-- Logic map dédiée -->
<script src="/theme/mobility-map-carousel.js"></script>
<script src="/theme/mobility-map-streetview.js"></script>

<!-- ToDo : Déplacer dans un fichier global ex db.js -->

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>

<script>
    window.ENV = {
        BACKEND_URL: "<?= getenv('INSTANCE_URL') ?>",
        BACKEND_PORT: "<?= getenv('BACKEND_PYTHON_PORT') ?>",
        USER_TOKEN: "<?= $_SESSION["jwt_token"] ?>",
        USER_ID: "<?= $_SESSION["id"] ?>"
    };
    console.log("Environnement chargé :", window.ENV);
</script>
<?php $t->endSlot(); ?>

<?php $t->startSlot('script.bottom'); ?>
<script type="module" defer>
    const map = L.map('map').setView([48.85, 2.35], 4);
    const submittedWishesByStudent = new Map();
    const expandedStudentRows = new Set();
    const expandedUniversityRows = new Set();
    const popupState = new Map();
    const wishesCountByUniversityId = new Map();
    window.MobilityMapState = {
        popupState,
        submittedWishesByStudent,
        semesters: [],
    };

    // In a flex layout, Leaflet can initialize before final dimensions are settled.
    requestAnimationFrame(() => map.invalidateSize());

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    const markers = L.markerClusterGroup();

    const fetchUniversityCatalog = async () => {
        const url = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + "/university/admin/catalog";
        let universities = [];
        try {
            const response = await fetch(url, {
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`,
                    "Content-Type": "application/json"
                }
            });
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            const data = await response.json();
            if (data && data.universities && data.semesters) {
                universities = data.universities;
                window.MobilityMapState.semesters = data.semesters;
            } else {
                universities = Array.isArray(data) ? data : [];
                window.MobilityMapState.semesters = [
                    { id: 4, label: "S8" },
                    { id: 5, label: "S9" }
                ];
            }
        } catch (error) {
            console.error(error.message);
            window.MobilityMapState.semesters = [
                { id: 4, label: "S8" },
                { id: 5, label: "S9" }
            ];
        }

        return universities;
    }

    const fetchWishes = async () => {
        const url = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + "/university/admin/wishes";
        let wishes = [];
        try {
            const response = await fetch(url, {
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`,
                    "Content-Type": "application/json"
                }
            });
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            wishes = await response.json();
        } catch (error) {
            console.error(error.message);
        }

        return wishes;
    }

    const universitiesById = new Map();
    const filieresById = new Map();
    const editableUniversities = [];

    window.MobilityMapState.universitiesById = universitiesById;
    window.MobilityMapState.filieresById = filieresById;

    function buildFiliereOptionsHtml() {
        return Array.from(filieresById.values())
            .sort((a, b) => String(a.nom_filiere).localeCompare(String(b.nom_filiere)))
            .map((filiere) => `<option value="${escapeHtml(String(filiere.id_filiere))}">${escapeHtml(filiere.nom_filiere || filiere.nom_long || 'Filiere')}</option>`)
            .join('');
    }

    function buildSemestreOptionsHtml() {
        const semesters = window.MobilityMapState.semesters || [
            { id: 4, label: "S8" },
            { id: 5, label: "S9" }
        ];
        return semesters
            .map((sem) => `<option value="${escapeHtml(String(sem.id))}">${escapeHtml(sem.label || `S${sem.id}`)}</option>`)
            .join('');
    }

    function hydrateCatalogState(universityCatalogRows) {
        universitiesById.clear();
        filieresById.clear();
        editableUniversities.splice(0, editableUniversities.length);

        for (const row of universityCatalogRows) {
            const uid = String(row.id_partner_university);
            if (!universitiesById.has(uid)) {
                universitiesById.set(uid, {
                    ...row,
                    filieres: [],
                    filiereIds: new Set(),
                    wishCount: 0,
                });
            }

            const university = universitiesById.get(uid);
            if (row.id_filiere !== null && row.id_filiere !== undefined) {
                const filiereId = String(row.id_filiere);
                university.filiereIds.add(filiereId);
                university.filieres.push({
                    id_filiere: row.id_filiere,
                    nom_filiere: row.nom_filiere,
                    nom_long: row.nom_long,
                    annee: row.annee,
                    number_of_places: row.number_of_places,
                });

                if (!filieresById.has(filiereId)) {
                    filieresById.set(filiereId, {
                        id_filiere: row.id_filiere,
                        nom_filiere: row.nom_filiere,
                        nom_long: row.nom_long,
                    });
                }
            }
        }

        const universities = Array.from(universitiesById.values()).map((university) => ({
            ...university,
            filieres: university.filieres.sort((a, b) => String(a.nom_filiere).localeCompare(String(b.nom_filiere))),
        }));

        editableUniversities.push(
            ...universities.map((u) => ({
                ...u,
                rowKey: String(u.id_partner_university),
                filiereIds: new Set(u.filiereIds || []),
                filieres: (u.filieres || []).map((f) => ({ ...f })),
                isDraft: false,
            }))
        );

        const filiereSelect = document.getElementById('filiereSelect');
        filiereSelect.innerHTML = '<option value="toutes">Toutes</option>' + buildFiliereOptionsHtml();
    }

    async function refreshWishesFromServer() {
        const wishes = await fetchWishes();
        submittedWishesByStudent.clear();
        wishesCountByUniversityId.clear();
        wishes.forEach((wish) => {
            const universityKey = String(wish.id_partner_university);
            wishesCountByUniversityId.set(universityKey, (wishesCountByUniversityId.get(universityKey) || 0) + 1);

            if (!submittedWishesByStudent.has(wish.id_etudiant)) {
                submittedWishesByStudent.set(wish.id_etudiant, {
                    student: {
                        id_etudiant: wish.id_etudiant,
                        nom: wish.etudiant_nom,
                        prenom: wish.etudiant_prenom,
                        mail: wish.etudiant_mail,
                        submission_date: wish.submission_date
                    },
                    wishes: []
                });
            }
            submittedWishesByStudent.get(wish.id_etudiant).wishes.push(wish);

            const catalogUniversity = universitiesById.get(String(wish.id_partner_university));
            if (catalogUniversity) {
                catalogUniversity.wishCount = wishesCountByUniversityId.get(String(wish.id_partner_university)) || 0;
            }
        });
    }
    async function refreshAllData() {
        const catalogRows = await fetchUniversityCatalog();
        hydrateCatalogState(catalogRows);
        await refreshWishesFromServer();
        refreshKpis();
        renderDashboardTable();
        renderUniversitiesAdminTable();
        updateMap();
    }

    function formatDateFR(dateValue) {
        if (!dateValue) return 'Non renseignee';
        const parsed = new Date(dateValue);
        if (Number.isNaN(parsed.getTime())) return 'Non renseignee';
        return parsed.toLocaleString('fr-FR');
    }

    function escapeHtml(value) {
        return String(value)
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#39;');
    }

    function getDashboardRows() {
        return Array.from(submittedWishesByStudent.values()).map((entry) => {
            const wishes = [...entry.wishes].sort((a, b) => (a.priority || 99) - (b.priority || 99));
            const submissionDate = entry.student.submission_date ? new Date(entry.student.submission_date) : null;
            const isRecent = submissionDate ? (Date.now() - submissionDate.getTime()) <= (7 * 24 * 60 * 60 * 1000) : false;
            // OLD CODE (Buggy: considérait parfois undefined ou "null" comme true)
            // const isSubmitted = Boolean(entry.student.submission_date);
            const isSubmitted = Boolean(entry.student.submission_date) && entry.student.submission_date !== 'null' && entry.student.submission_date !== 'None';
            const status = isSubmitted && wishes.length >= 5 ? 'complet' : 'incomplet';

            return {
                studentId: entry.student.id_etudiant,
                fullname: `${entry.student.prenom || ''} ${entry.student.nom || ''}`.trim(),
                email: entry.student.mail || '',
                submissionDate,
                submissionDateText: formatDateFR(entry.student.submission_date),
                wishes,
                wishesCount: wishes.length,
                status,
                isSubmitted,
                isRecent,
            };
        });
    }

    function statusBadge(status) {
        if (status === 'complet') {
            return { label: 'Complet', className: 'bg-green-100 text-green-700' };
        }
        return { label: 'Incomplet', className: 'bg-yellow-100 text-yellow-700' };
    }

    window.toggleWishDetails = function (studentId) {
        const key = String(studentId);
        if (expandedStudentRows.has(key)) {
            expandedStudentRows.delete(key);
        } else {
            expandedStudentRows.add(key);
        }
        renderDashboardTable();
    };

    function renderDashboardTable() {
        const body = document.getElementById('wishesTableBody');
        const query = (document.getElementById('wishesSearch').value || '').trim().toLowerCase();
        const statusFilter = document.getElementById('dossierStatusFilter').value;

        let rows = getDashboardRows();

        if (statusFilter !== 'tous') {
            rows = rows.filter((row) => {
                if (statusFilter === 'recent') return row.isRecent;
                return row.status === statusFilter;
            });
        }

        if (query) {
            rows = rows.filter((row) => {
                const searchable = [
                    row.fullname,
                    row.email,
                    ...row.wishes.map((w) => {
                        const uid = String(w.id_partner_university || '');
                        const uni = universitiesById.get(uid);
                        return uni ? `${uni.name} ${uni.country || ''}` : (w.university_name || '');
                    }),
                ].join(' ').toLowerCase();

                return searchable.includes(query);
            });
        }

        rows.sort((a, b) => {
            if (!a.submissionDate && !b.submissionDate) return 0;
            if (!a.submissionDate) return 1;
            if (!b.submissionDate) return -1;
            return b.submissionDate - a.submissionDate;
        });

        const countText = rows.length + ' resultat' + (rows.length > 1 ? 's' : '');
        document.getElementById('wishesResultsCount').innerText = countText;

        if (rows.length === 0) {
            body.innerHTML = '<tr><td colspan="5" class="px-6 py-12 text-center text-gray-500">Aucun dossier ne correspond aux filtres.</td></tr>';
            return;
        }

        const html = rows.map((row) => {
            const badge = statusBadge(row.status);
            const studentRowKey = String(row.studentId || '');
            const isExpanded = expandedStudentRows.has(studentRowKey);
            const firstWish = row.wishes[0] || null;
            const initials = row.fullname
                .split(' ')
                .filter(Boolean)
                .map((word) => word[0].toUpperCase())
                .join('')
                .slice(0, 3);
            const wishRows = row.wishes.slice(0, 5).map((wish, index) => {
                const wishId = String(wish.id_partner_university || '');
                const uni = universitiesById.get(wishId);
                const wishName = uni ? uni.name : (wish.university_name || `Universite ${wishId}`);
                const wishCountry = uni ? uni.country : (wish.university_country || '');
                const wishCode = uni ? uni.code : (wish.university_code || '');

                return `
                    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 rounded-lg border border-gray-200 bg-white p-3">
                        <div class="min-w-0">
                            <div class="text-sm font-semibold text-gray-900">#${index + 1} - ${escapeHtml(wishName)}</div>
                            <div class="text-xs text-gray-500">${escapeHtml(wishCountry)} - ${escapeHtml(wishCode || '')}</div>
                        </div>
                        <button type="button" class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg text-blue-700 bg-blue-50 hover:bg-blue-100 transition shrink-0" onclick="window.scrollToUniversityOnMap('${escapeHtml(wishId)}')">Voir sur la carte</button>
                    </div>
                `;
            }).join('');

            return `
                <tr class="hover:bg-gray-100 transition">
                    <td class="px-6 py-4">
                        <div class="flex items-center gap-3">
                            <div class="w-9 h-9 rounded-full bg-blue-100 flex items-center justify-center shrink-0">
                                <span class="text-xs font-bold text-blue-600">${escapeHtml(initials || 'NA')}</span>
                            </div>
                            <div>
                                <div class="font-semibold text-gray-900">${escapeHtml(row.fullname || 'Etudiant')}</div>
                                <div class="text-xs text-gray-500">${escapeHtml(row.email || '-')}</div>
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-gray-600">${escapeHtml(row.submissionDateText)}</td>
                    <td class="px-6 py-4">
                        <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ${badge.className}">${badge.label}</span>
                    </td>
                    <td class="px-6 py-4 text-gray-900 font-semibold">${row.wishesCount}/5</td>
                    <td class="px-6 py-4">
                        <div class="flex items-center justify-end gap-2">
                            <button type="button" class="inline-flex items-center justify-center w-8 h-8 rounded-full border border-gray-300 text-gray-600 hover:bg-gray-100 transition" onclick="window.toggleWishDetails('${escapeHtml(studentRowKey)}')" aria-label="Afficher les voeux">
                                <svg class="w-4 h-4 transition ${isExpanded ? 'rotate-180' : ''}" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
                            </button>
                        </div>
                    </td>
                </tr>
                ${isExpanded ? `
                <tr class="bg-gray-50">
                    <td colspan="5" class="px-6 py-4">
                        <div class="space-y-2">
                            ${wishRows || '<div class="text-sm text-gray-500">Aucun voeu enregistre.</div>'}
                        </div>
                    </td>
                </tr>
                ` : ''}
            `;
        }).join('');

        body.innerHTML = html;
    }

    function getSemesterLabel(annee) {
        return Number(annee) === 4 ? 'S8' : 'S9';
    }

    function renderUniversitiesAdminTable() {
        const body = document.getElementById('universitiesAdminBody');
        const query = (document.getElementById('universityAdminSearch').value || '').trim().toLowerCase();

        let rows = [...editableUniversities];
        if (query) {
            rows = rows.filter((u) => {
                const text = [u.name, u.country, u.code, u.website].join(' ').toLowerCase();
                return text.includes(query);
            });
        }

        rows.sort((a, b) => String(a.name || '').localeCompare(String(b.name || '')));

        if (rows.length === 0) {
            body.innerHTML = '<tr><td colspan="5" class="px-6 py-10 text-center text-gray-500">Aucune universite ne correspond a la recherche.</td></tr>';
            return;
        }

        body.innerHTML = rows.map((u) => {
            const key = String(u.rowKey);
            const isExpanded = expandedUniversityRows.has(key);
            const wishesCount = wishesCountByUniversityId.get(String(u.id_partner_university || '')) || 0;
            const filiereRows = (u.filieres || []).map((f, index) => {
                const filiereText = f.nom_filiere || f.nom_long || `Filiere ${f.id_filiere}`;
                return `
                    <div class="grid grid-cols-1 lg:grid-cols-[2fr_1fr_auto] gap-2 items-center rounded border border-gray-200 bg-white p-2">
                        <div class="text-xs text-gray-700">${escapeHtml(filiereText)} - ${escapeHtml(getSemesterLabel(f.annee))}</div>
                        <input type="number" min="0" value="${escapeHtml(String(f.number_of_places ?? 0))}" class="border rounded px-2 py-1 text-xs" onchange="window.updateUniversityPlace('${escapeHtml(key)}', ${index}, this.value)" />
                        <button type="button" class="text-xs px-2 py-1 rounded bg-red-50 text-red-700 hover:bg-red-100" onclick="window.removeUniversityPlace('${escapeHtml(key)}', ${index})">Supprimer</button>
                    </div>
                `;
            }).join('');

            return `
                <tr class="hover:bg-gray-100 transition">
                    <td class="px-6 py-4">
                        <div class="font-semibold text-gray-900">${escapeHtml(u.name || 'Nouvelle universite')}</div>
                    </td>
                    <td class="px-6 py-4 text-gray-600">${escapeHtml(u.country || '-')}</td>
                    <td class="px-6 py-4 text-gray-600">${escapeHtml(u.code || '-')}</td>
                    <td class="px-6 py-4 text-gray-900 font-semibold">${escapeHtml(String(wishesCount))}</td>
                    <td class="px-6 py-4">
                        <div class="flex items-center justify-end gap-2">
                            <button type="button" class="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg text-blue-700 bg-blue-50 hover:bg-blue-100 transition" onclick="window.toggleUniversityPlacesEditor('${escapeHtml(key)}')">Editer les places</button>
                        </div>
                    </td>
                </tr>
                ${isExpanded ? `
                <tr class="bg-gray-50">
                    <td colspan="5" class="px-6 py-4">
                        <div class="space-y-3">
                            <div class="grid grid-cols-1 lg:grid-cols-3 gap-2">
                                <input type="text" value="${escapeHtml(u.name || '')}" placeholder="Nom universite" class="border rounded px-2 py-1 text-xs" onchange="window.updateUniversityMeta('${escapeHtml(key)}', 'name', this.value)" />
                                <input type="text" value="${escapeHtml(u.country || '')}" placeholder="Pays" class="border rounded px-2 py-1 text-xs" onchange="window.updateUniversityMeta('${escapeHtml(key)}', 'country', this.value)" />
                                <input type="text" value="${escapeHtml(u.code || '')}" placeholder="Code" class="border rounded px-2 py-1 text-xs" onchange="window.updateUniversityMeta('${escapeHtml(key)}', 'code', this.value)" />
                            </div>

                            <div class="flex flex-wrap items-center gap-2">
                                <select id="addPlaceFiliere-${escapeHtml(key)}" class="border rounded px-2 py-1 text-xs">
                                    ${Array.from(filieresById.values()).sort((a, b) => String(a.nom_filiere).localeCompare(String(b.nom_filiere))).map((f) => `<option value="${escapeHtml(String(f.id_filiere))}">${escapeHtml(f.nom_filiere || f.nom_long || 'Filiere')}</option>`).join('')}
                                </select>
                                <select id="addPlaceSemestre-${escapeHtml(key)}" class="border rounded px-2 py-1 text-xs">
                                    ${buildSemestreOptionsHtml()}
                                </select>
                                <button type="button" class="text-xs px-2 py-1 rounded bg-gray-200 text-gray-700 hover:bg-gray-300" onclick="window.addUniversityPlace('${escapeHtml(key)}')">Ajouter une place</button>
                            </div>

                            <div class="space-y-2">
                                ${filiereRows || '<div class="text-xs text-gray-500">Aucune place configuree.</div>'}
                            </div>

                            <div class="flex items-center justify-end gap-2">
                                <button type="button" class="text-xs px-3 py-1.5 rounded bg-green-600 text-white hover:bg-green-700" onclick="window.saveUniversityDraft('${escapeHtml(key)}')">Enregistrer</button>
                            </div>
                        </div>
                    </td>
                </tr>
                ` : ''}
            `;
        }).join('');
    }

    function getEditableUniversityByKey(rowKey) {
        return editableUniversities.find((u) => String(u.rowKey) === String(rowKey));
    }

    async function parseApiError(response) {
        try {
            const data = await response.json();
            return data?.detail || `Erreur ${response.status}`;
        } catch {
            return `Erreur ${response.status}`;
        }
    }

    window.toggleUniversityPlacesEditor = function (rowKey) {
        const key = String(rowKey);
        if (expandedUniversityRows.has(key)) {
            expandedUniversityRows.delete(key);
        } else {
            expandedUniversityRows.add(key);
        }
        renderUniversitiesAdminTable();
    };

    window.updateUniversityMeta = function (rowKey, field, value) {
        const university = getEditableUniversityByKey(rowKey);
        if (!university) return;
        university[field] = value;
    };

    window.updateUniversityPlace = function (rowKey, placeIndex, value) {
        const university = getEditableUniversityByKey(rowKey);
        if (!university || !university.filieres[placeIndex]) return;
        const parsed = Number.parseInt(value, 10);
        university.filieres[placeIndex].number_of_places = Number.isNaN(parsed) ? 0 : Math.max(0, parsed);
        const firstPlace = university.filieres[0];
        if (firstPlace) {
            university.number_of_places = firstPlace.number_of_places;
            university.annee = firstPlace.annee;
        }
        updateMap();
    };

    window.removeUniversityPlace = function (rowKey, placeIndex) {
        const university = getEditableUniversityByKey(rowKey);
        if (!university) return;
        university.filieres.splice(placeIndex, 1);
        university.filiereIds = new Set(university.filieres.map((f) => String(f.id_filiere)));
        renderUniversitiesAdminTable();
        updateMap();
    };

    window.addUniversityPlace = function (rowKey) {
        const university = getEditableUniversityByKey(rowKey);
        if (!university) return;
        const filiereSelectEl = document.getElementById(`addPlaceFiliere-${rowKey}`);
        const semestreSelectEl = document.getElementById(`addPlaceSemestre-${rowKey}`);
        if (!filiereSelectEl || !semestreSelectEl) return;

        const filiereId = String(filiereSelectEl.value);
        const filiereMeta = filieresById.get(filiereId);
        const annee = Number.parseInt(semestreSelectEl.value, 10);

        university.filieres.push({
            id_filiere: Number.parseInt(filiereId, 10),
            nom_filiere: filiereMeta?.nom_filiere || 'Filiere',
            nom_long: filiereMeta?.nom_long || '',
            annee,
            number_of_places: 1,
        });
        university.filiereIds.add(filiereId);
        const firstPlace = university.filieres[0];
        if (firstPlace) {
            university.number_of_places = firstPlace.number_of_places;
            university.annee = firstPlace.annee;
        }

        renderUniversitiesAdminTable();
        updateMap();
    };

    window.saveUniversityDraft = async function (rowKey) {
        const university = getEditableUniversityByKey(rowKey);
        if (!university) return;

        const payload = {
            name: String(university.name || '').trim(),
            country: String(university.country || '').trim(),
            code: university.code || null,
            address: university.address || null,
            latitude: Number(university.latitude || 0),
            longitude: Number(university.longitude || 0),
            website: university.website || null,
            languages: university.languages || null,
            note_min: university.note_min === null || university.note_min === undefined || university.note_min === ''
                ? null
                : Number(university.note_min),
            type: university.type || 'ERASMUS',
            places: (university.filieres || []).map((f) => ({
                id_filiere: Number(f.id_filiere),
                annee: Number(f.annee),
                number_of_places: Math.max(0, Number.parseInt(f.number_of_places ?? 0, 10) || 0),
            })),
        };

        if (!payload.name || !payload.country) {
            window.alert('Nom et pays sont obligatoires.');
            return;
        }

        const url = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + `/university/admin/${university.id_partner_university}`;
        const method = 'PUT';

        const response = await fetch(url, {
            method,
            headers: {
                'Authorization': `Bearer ${window.ENV.USER_TOKEN}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const detail = await parseApiError(response);
            window.alert(`Enregistrement impossible: ${detail}`);
            return;
        }
        await refreshAllData();
    };

    function refreshKpis() {
        const rows = getDashboardRows();
        const submittedCount = rows.filter((row) => row.isSubmitted).length;
        const incompleteCount = rows.filter((row) => !row.isSubmitted).length;
        const recentCount = rows.filter((row) => row.isRecent && row.isSubmitted).length;
        const targetedUniversitiesCount = new Set(
            rows.flatMap((row) => row.wishes.map((wish) => String(wish.id_partner_university || '')))
                .filter(Boolean)
        ).size;

        document.getElementById('kpiStudents').innerText = String(submittedCount);
        document.getElementById('kpiIncomplete').innerText = String(incompleteCount);
        document.getElementById('kpiUniversities').innerText = String(targetedUniversitiesCount);
        document.getElementById('kpiRecent').innerText = String(recentCount);
    }

    function getLanguageFlags(languagesString) {
        if (!languagesString) return '';
        const flags = {
            'Allemand': '🇩🇪',
            'Anglais': '🇬🇧',
            'Espagnol': '🇪🇸',
            'Français': '🇫🇷',
            'Portugais': '🇵🇹',
            'Italien': '🇮🇹',
            'Japonais': '🇯🇵'
        };

        return languagesString.split(',').map(l => {
            const lang = l.trim();
            return flags[lang] ? `<span title="${escapeHtml(lang)}" class="text-base cursor-help">${flags[lang]}</span>` : escapeHtml(lang);
        }).join(' ');
    }

    function popupText(university) {
        const uid = String(university.id_partner_university);

        window.MobilityMapState.popupState.set(uid, {
            photos: null,
            photoIndex: 0,
            streetView: null
        });

        return `
            <div class="popup-tabs">
                <button id="tab-photos-${uid}" type="button" class="popup-tab" onclick="window.switchPopupTab('${uid}', 'photos')">Photos</button>
                <button id="tab-street-${uid}" type="button" class="popup-tab" onclick="window.switchPopupTab('${uid}', 'streetview')">StreetView</button>
            </div>
            <div id="panel-photos-${uid}" class="popup-panel hidden">
                <div class="popup-carousel">
                    <div class="popup-photo-frame">
                        <img id="photo-image-${uid}" class="popup-photo" alt="Photo universite" />
                        <button id="photo-prev-${uid}" type="button" class="popup-carousel-btn left" onclick="window.prevPopupPhoto('${uid}')" disabled>‹</button>
                        <button id="photo-next-${uid}" type="button" class="popup-carousel-btn right" onclick="window.nextPopupPhoto('${uid}')" disabled>›</button>
                    </div>
                </div>
                <p id="photo-caption-${uid}" class="popup-photo-caption"></p>
                <p id="photo-status-${uid}" class="popup-status">Chargement des photos...</p>
            </div>
            <div id="panel-street-${uid}" class="popup-panel hidden">
                <div id="streetview-${uid}" class="popup-streetview"></div>
                <p id="street-status-${uid}" class="popup-status">Chargement du Street View...</p>
                <div class="popup-streetview-actions">
                    <button id="street-open-${uid}" type="button" class="popup-streetview-expand" onclick="window.openStreetViewModal('${uid}')" disabled>Ouvrir en grand</button>
                </div>
            </div>
            <b>${escapeHtml(university.name)}</b> (${escapeHtml(university.code)})<br/>
            <em class="text-[0.75rem]">${escapeHtml(university.address)}, ${escapeHtml(university.country)}</em><br/>
            ${getLanguageFlags(university.languages)}<br/>
            S${university.annee == 4 ? '8' : '9'} : 
            ${escapeHtml(university.number_of_places)} place${university.number_of_places > 1 ? 's' : ''}<br/>
            Demandes sur cette universite : ${escapeHtml(String(wishesCountByUniversityId.get(uid) || 0))}<br/>
            ${university.note_min !== null ? `Note min : ${university.note_min}<br/>` : ''}
            <a href="${escapeHtml(university.website)}" target="_blank">${escapeHtml(university.website)}</a><br/>
            
        `;
    }

    function resetAddUniversityForm() {
        document.getElementById('newUniName').value = '';
        document.getElementById('newUniCountry').value = '';
        document.getElementById('newUniCode').value = '';
        document.getElementById('newUniAddress').value = '';
        document.getElementById('newUniWebsite').value = '';
        document.getElementById('newUniLanguages').value = 'Anglais';
        document.getElementById('newUniLatitude').value = '48.85';
        document.getElementById('newUniLongitude').value = '2.35';
        document.getElementById('newUniNoteMin').value = '';
        document.getElementById('newUniType').value = 'ERASMUS';
        const placesRows = document.getElementById('newUniPlacesRows');
        placesRows.innerHTML = '';
        window.addNewUniversityPlaceRow();
    }

    window.addNewUniversityPlaceRow = function () {
        const rowId = `new-place-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
        const rowHtml = `
            <div id="${rowId}" class="grid grid-cols-1 lg:grid-cols-[2fr_1fr_1fr_auto] gap-2 items-center">
                <select class="new-uni-place-filiere border rounded px-2 py-1 text-xs">${buildFiliereOptionsHtml()}</select>
                <select class="new-uni-place-annee border rounded px-2 py-1 text-xs">
                    ${buildSemestreOptionsHtml()}
                </select>
                <input type="number" min="0" value="1" class="new-uni-place-count border rounded px-2 py-1 text-xs" />
                <button type="button" class="text-xs px-2 py-1 rounded bg-red-50 text-red-700 hover:bg-red-100" onclick="document.getElementById('${rowId}').remove()">Supprimer</button>
            </div>
        `;
        document.getElementById('newUniPlacesRows').insertAdjacentHTML('beforeend', rowHtml);
    };

    function collectNewUniversityPlaces() {
        const placeRows = Array.from(document.querySelectorAll('#newUniPlacesRows > div'));
        return placeRows.map((row) => {
            const filiere = row.querySelector('.new-uni-place-filiere');
            const annee = row.querySelector('.new-uni-place-annee');
            const count = row.querySelector('.new-uni-place-count');
            return {
                id_filiere: Number(filiere?.value || 0),
                annee: Number(annee?.value || 4),
                number_of_places: Math.max(0, Number.parseInt(count?.value || '0', 10) || 0),
            };
        });
    }

    window.saveNewUniversity = async function () {
        const payload = {
            name: document.getElementById('newUniName').value.trim(),
            country: document.getElementById('newUniCountry').value.trim(),
            code: document.getElementById('newUniCode').value.trim() || null,
            address: document.getElementById('newUniAddress').value.trim() || null,
            website: document.getElementById('newUniWebsite').value.trim() || null,
            languages: document.getElementById('newUniLanguages').value.trim() || null,
            latitude: Number(document.getElementById('newUniLatitude').value || 0),
            longitude: Number(document.getElementById('newUniLongitude').value || 0),
            note_min: document.getElementById('newUniNoteMin').value === '' ? null : Number(document.getElementById('newUniNoteMin').value),
            type: document.getElementById('newUniType').value || 'ERASMUS',
            places: collectNewUniversityPlaces(),
        };

        if (!payload.name || !payload.country) {
            window.alert('Nom et pays sont obligatoires.');
            return;
        }

        const response = await fetch((window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + '/university/admin', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${window.ENV.USER_TOKEN}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const detail = await parseApiError(response);
            window.alert(`Creation impossible: ${detail}`);
            return;
        }

        document.getElementById('addUniversityPanel').classList.add('hidden');
        await refreshAllData();
        resetAddUniversityForm();
    };



    window.flyToUniversity = function (uid) {
        const university = universitiesById.get(String(uid));
        if (!university) return;

        const marker = window.MobilityMapState.markerInstances && window.MobilityMapState.markerInstances.get(String(uid));
        if (marker) {
            markers.zoomToShowLayer(marker, () => {
                marker.openPopup();
            });
        } else {
            // Le marqueur est filtré : on désactive les filtres pour l'afficher
            document.getElementById('semestreSelect').value = 'Tous';
            document.getElementById('filiereSelect').value = 'toutes';
            const range = document.getElementById('noteMinRange');
            range.value = 20;
            document.getElementById('noteMinValue').innerText = 20;
            updateMap();

            // On retente la navigation et l'ouverture lorsque la carte est à jour
            setTimeout(() => {
                window.flyToUniversity(uid);
            }, 100);
        }
    };

    window.scrollToUniversityOnMap = function (uid) {
        const mapSection = document.getElementById('mapSection');
        mapSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        window.setTimeout(() => {
            window.flyToUniversity(uid);
        }, 250);
    };

    function updateMap() {
        markers.clearLayers();
        window.MobilityMapState.markerInstances = new Map();

        const selectedSemestre = document.getElementById('semestreSelect').value;
        const selectedFiliere = document.getElementById('filiereSelect').value;
        const selectedNote = parseFloat(document.getElementById('noteMinRange').value);

        const filtered = editableUniversities.filter(u => {
            // Affiche univ si note_min <= selectedNote
            const uNote = u.note_min === null ? 0 : parseFloat(u.note_min);
            if (uNote > selectedNote) return false;

            if (selectedFiliere !== 'toutes' && (!u.filiereIds || !u.filiereIds.has(String(selectedFiliere)))) {
                return false;
            }

            // Filtre le semestre
            if (selectedSemestre === "S8") {
                return u.annee === 4;
            } else if (selectedSemestre === "S9") {
                return u.annee === 5;
            } else {
                return true;
            }
        });

        filtered.forEach(university => {
            const marker = L.marker([university.latitude, university.longitude])
                .bindPopup(popupText(university));

            marker.on('popupopen', () => {
                void window.hydratePopupContent(university);
            });

            window.MobilityMapState.markerInstances.set(String(university.id_partner_university), marker);
            markers.addLayer(marker);
        });
        map.addLayer(markers);
    }

    window.updateMap = updateMap; // Pour pouvoir appeler depuis le PHP

    document.getElementById('wishesSearch').addEventListener('input', renderDashboardTable);
    document.getElementById('dossierStatusFilter').addEventListener('change', renderDashboardTable);
    document.getElementById('filiereSelect').addEventListener('change', updateMap);
    document.getElementById('universityAdminSearch').addEventListener('input', renderUniversitiesAdminTable);
    document.getElementById('addUniversityRowBtn').addEventListener('click', () => {
        const panel = document.getElementById('addUniversityPanel');
        panel.classList.toggle('hidden');
    });
    document.getElementById('cancelAddUniversityBtn').addEventListener('click', () => {
        document.getElementById('addUniversityPanel').classList.add('hidden');
    });
    document.getElementById('addNewUniPlaceRowBtn').addEventListener('click', window.addNewUniversityPlaceRow);
    document.getElementById('saveNewUniversityBtn').addEventListener('click', window.saveNewUniversity);
    document.getElementById('resetDashboardFilters').addEventListener('click', () => {
        document.getElementById('wishesSearch').value = '';
        document.getElementById('dossierStatusFilter').value = 'tous';
        document.getElementById('filiereSelect').value = 'toutes';
        document.getElementById('semestreSelect').value = 'Tous';
        document.getElementById('noteMinRange').value = 20;
        document.getElementById('noteMinValue').innerText = 20;
        renderDashboardTable();
        updateMap();
    });

    resetAddUniversityForm();
    await refreshAllData();

    window.forceSubmitWishesExec = async function () {
        if (!confirm("Êtes-vous sûr de vouloir forcer la clôture de tous les dossiers de vœux incomplets ?\n\nTous les étudiants ayant fait au moins 1 choix verront leur dossier verrouillé et soumis.")) return;

        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/wishes/force-submit", {
                method: 'POST',
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`,
                    "Content-Type": "application/json"
                }
            });

            if (!response.ok) {
                const err = await parseApiError(response);
                alert("Erreur: " + err);
                return;
            }

            alert("Tous les vœux incomplets ont été clôturés avec succès.");
            refreshAllData();
        } catch (error) {
            alert("Erreur de connexion.");
        }
    };

    window.mobilityQuotas = [];
    window.globalFilieres = [];

    window.fetchGlobalFilieres = async function () {
        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/filieres/", {
                headers: { "Authorization": `Bearer ${window.ENV.USER_TOKEN}` }
            });
            if (response.ok) {
                window.globalFilieres = await response.json();
                const select = document.getElementById('quotaMobilityFiliere');
                if (select) {
                    select.innerHTML = window.globalFilieres
                        .sort((a, b) => String(a.nom_filiere).localeCompare(String(b.nom_filiere)))
                        .map(f => `<option value="${f.id_filiere}">${f.nom_filiere || f.nom_long}</option>`)
                        .join('');
                }
            }
        } catch (e) {
            console.error("Erreur chargement filières", e);
        }
    };

    window.addMobilityQuota = function () {
        const id_filiere = parseInt(document.getElementById('quotaMobilityFiliere').value, 10);
        const id_semestre = parseInt(document.getElementById('quotaMobilitySemester').value, 10);
        const places = parseInt(document.getElementById('quotaMobilityPlaces').value, 10);

        if (isNaN(id_filiere) || isNaN(id_semestre) || isNaN(places) || places < 0) {
            alert("Veuillez remplir tous les champs correctement.");
            return;
        }

        const exists = window.mobilityQuotas.find(q => q.id_filiere === id_filiere && q.id_semestre === id_semestre);
        if (exists) {
            alert("Un quota pour cette filière et ce semestre existe déjà. Veuillez le supprimer pour le modifier.");
            return;
        }

        window.mobilityQuotas.push({ id_filiere, id_semestre, places });
        window.renderMobilityQuotas();
    };

    window.removeMobilityQuota = function (index) {
        window.mobilityQuotas.splice(index, 1);
        window.renderMobilityQuotas();
    };

    window.renderMobilityQuotas = function () {
        const container = document.getElementById('mobilityQuotasList');
        const emptyMsg = document.getElementById('mobilityQuotasEmpty');

        // Clear old list items except empty message
        Array.from(container.children).forEach(child => {
            if (child.id !== 'mobilityQuotasEmpty') {
                child.remove();
            }
        });

        if (window.mobilityQuotas.length === 0) {
            emptyMsg.classList.remove('hidden');
        } else {
            emptyMsg.classList.add('hidden');
            window.mobilityQuotas.forEach((q, i) => {
                const f = window.globalFilieres.find(f => f.id_filiere === q.id_filiere);
                const nom = f ? (f.nom_filiere || f.nom_long) : `Filière ${q.id_filiere}`;

                const item = document.createElement('div');
                item.className = "flex justify-between items-center bg-white p-2 border border-gray-200 rounded shadow-sm text-xs";
                item.innerHTML = `
                    <div class="font-semibold text-gray-700">
                        ${nom} <span class="text-indigo-600 bg-indigo-50 px-1.5 py-0.5 rounded ml-1">S${q.id_semestre}</span>
                    </div>
                    <div class="flex items-center gap-3">
                        <span class="font-bold text-gray-800">${q.places} place(s)</span>
                        <button onclick="window.removeMobilityQuota(${i})" class="text-red-500 hover:text-red-700 transition">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                        </button>
                    </div>
                `;
                container.appendChild(item);
            });
        }

        // Update quota counter
        const counterEl = document.getElementById('quotaCounter');
        if (counterEl && window.globalFilieres) {
            const totalPossible = window.globalFilieres.length * 2; // 2 semesters per filière
            const filled = window.mobilityQuotas.length;
            counterEl.textContent = `${filled} / ${totalPossible} quotas configurés`;

            if (filled === totalPossible && totalPossible > 0) {
                counterEl.classList.remove('text-gray-600', 'bg-gray-100', 'border-gray-200');
                counterEl.classList.add('text-emerald-700', 'bg-emerald-100', 'border-emerald-300');
            } else {
                counterEl.classList.add('text-gray-600', 'bg-gray-100', 'border-gray-200');
                counterEl.classList.remove('text-emerald-700', 'bg-emerald-100', 'border-emerald-300');
            }
        }
    };

    let assignmentPollInterval = null;

    function startAssignmentPolling() {
        if (assignmentPollInterval) clearInterval(assignmentPollInterval);

        assignmentPollInterval = setInterval(async () => {
            try {
                const res = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/assignment/status", {
                    method: 'GET',
                    headers: { "Authorization": `Bearer ${window.ENV.USER_TOKEN}` }
                });

                if (res.ok) {
                    const status = await res.json();

                    document.getElementById('assignmentProgressBar').style.width = `${status.progress}%`;
                    document.getElementById('assignmentProgressPercent').innerText = `${status.progress}%`;
                    document.getElementById('assignmentProgressText').innerText = status.step;

                    if (status.error) {
                        clearInterval(assignmentPollInterval);
                        alert("Erreur dans l'algorithme : " + status.error);
                        resetAssignmentUI();
                    } else if (status.progress >= 100 || !status.is_running) {
                        clearInterval(assignmentPollInterval);
                        setTimeout(() => {
                            document.getElementById('procedureModal').classList.add('hidden');
                            alert("Algorithme terminé ! (Affectations enregistrées)");
                            resetAssignmentUI();
                            refreshAllData();
                        }, 500);
                    }
                }
            } catch (e) {
                console.error("Polling error", e);
            }
        }, 500);
    }

    function resetAssignmentUI() {
        document.getElementById('assignmentActions').classList.remove('hidden');
        document.getElementById('assignmentProgressContainer').classList.add('hidden');
        document.getElementById('assignmentProgressBar').style.width = '0%';
        document.getElementById('assignmentProgressPercent').innerText = '0%';
        document.getElementById('assignmentProgressText').innerText = 'Démarrage...';
    }

    window.runAssignmentExec = async function () {
        const payload = {
            annee_eligible: 4, // Procédure exclusive aux 4ème année
            mobility_quotas: window.mobilityQuotas
        };

        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/assignment/run", {
                method: 'POST',
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const err = await parseApiError(response);
                alert("Erreur lors de l'affectation: " + err);
                return;
            }

            document.getElementById('assignmentActions').classList.add('hidden');
            document.getElementById('assignmentProgressContainer').classList.remove('hidden');

            startAssignmentPolling();
        } catch (error) {
            alert("Erreur de connexion.");
        }
    };

    window.exportWishes = async function () {
        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/wishes/export", {
                method: 'GET',
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`
                }
            });
            if (!response.ok) {
                alert("Erreur lors de l'exportation des vœux");
                return;
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `Export_Voeux_Mobilite_${new Date().toISOString().slice(0, 10)}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            alert("Erreur de connexion.");
        }
    };

    window.exportAssignments = async function () {
        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/assignments/export", {
                method: 'GET',
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`
                }
            });
            if (!response.ok) {
                alert("Erreur lors de l'exportation des affectations");
                return;
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `Export_Affectations_Mobilite_${new Date().toISOString().slice(0, 10)}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            alert("Erreur de connexion.");
        }
    };

    window.exportPlaces = async function () {
        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/places/export", {
                method: 'GET',
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`
                }
            });
            if (!response.ok) {
                alert("Erreur lors de l'exportation de l'état des places");
                return;
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `Export_Etat_Places_${new Date().toISOString().slice(0, 10)}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            alert("Erreur de connexion.");
        }
    };

    // Procedure Modal & Reset Logic
    window.openProcedureModal = function () {
        document.getElementById('procedureModal').classList.remove('hidden');
        window.fetchSubmittedStudents();
        window.fetchAssignedStudents();
        window.fetchGlobalFilieres();
    };

    window.submittedStudentsList = [];

    window.fetchSubmittedStudents = async function () {
        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/mobility/submitted-students", {
                headers: { "Authorization": `Bearer ${window.ENV.USER_TOKEN}` }
            });
            if (response.ok) {
                window.submittedStudentsList = await response.json();

                // Populate Reset Student Dropdown
                const select = document.getElementById('resetStudentSelect');
                select.innerHTML = '<option value="">Sélectionnez un étudiant...</option>';
                window.submittedStudentsList.forEach(student => {
                    const opt = document.createElement('option');
                    opt.value = student.id_etudiant;
                    opt.textContent = `${student.id_etudiant} - ${student.nom} ${student.prenom}`;
                    select.appendChild(opt);
                });
                document.getElementById('resetStudentDetails').classList.add('hidden');
                document.getElementById('btnResetWishes').classList.add('hidden');

                // Populate Filiere Quotas
                const filieres = [...new Set(window.submittedStudentsList.map(s => s.nom_filiere))].filter(Boolean).sort();
                const container = document.getElementById('filiereQuotasContainer');
                if (filieres.length > 0) {
                    container.innerHTML = '';
                    filieres.forEach(filiere => {
                        const id_safe = 'quota_' + filiere.replace(/[^a-zA-Z0-9]/g, '_');
                        container.innerHTML += `
                            <div class="bg-white border border-gray-200 rounded p-2 flex flex-col justify-between">
                                <label for="${id_safe}" class="text-xs font-semibold text-gray-700 mb-1 truncate" title="${filiere}">${filiere}</label>
                                <input type="number" id="${id_safe}" data-filiere="${filiere}" class="filiere-quota-input w-full text-sm border-gray-300 rounded px-2 py-1" value="0" min="0">
                            </div>
                        `;
                    });
                } else {
                    container.innerHTML = '<span class="text-xs text-gray-400 italic">Aucune filière trouvée.</span>';
                }
            }
        } catch (error) {
            console.error("Erreur chargement des étudiants soumis", error);
        }
    };

    window.onResetStudentChange = function () {
        const select = document.getElementById('resetStudentSelect');
        const id = select.value;
        const detailsDiv = document.getElementById('resetStudentDetails');
        const btn = document.getElementById('btnResetWishes');

        if (!id) {
            detailsDiv.classList.add('hidden');
            btn.classList.add('hidden');
            return;
        }

        const student = window.submittedStudentsList.find(s => s.id_etudiant == id);
        if (student) {
            document.getElementById('rsName').textContent = `${student.nom} ${student.prenom}`;
            document.getElementById('rsEmail').textContent = student.mail;
            document.getElementById('rsFiliere').textContent = student.nom_filiere;
            detailsDiv.classList.remove('hidden');
            btn.classList.remove('hidden');
        }
    };

    window.resetStudentWishes = async function () {
        const select = document.getElementById('resetStudentSelect');
        const id = select.value;
        if (!id) return;

        if (!confirm("Êtes-vous sûr de vouloir annuler la soumission de cet étudiant ? Il repassera en statut 'En cours'.")) {
            return;
        }

        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/mobility/reset-wishes/" + id, {
                method: 'POST',
                headers: { "Authorization": `Bearer ${window.ENV.USER_TOKEN}` }
            });

            if (response.ok) {
                alert("Soumission annulée avec succès.");
                window.fetchSubmittedStudents();
                if (typeof refreshAllData === 'function') {
                    refreshAllData();
                }
            } else {
                alert("Erreur lors de l'annulation.");
            }
        } catch (error) {
            alert("Erreur de connexion.");
        }
    };

    // --- Validation manuelle des affectations (Etape 3) ---
    window.assignedStudentsList = [];

    window.fetchAssignedStudents = async function () {
        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/mobility/assigned-students", {
                headers: { "Authorization": `Bearer ${window.ENV.USER_TOKEN}` }
            });
            if (response.ok) {
                window.assignedStudentsList = await response.json();

                const select = document.getElementById('validationStudentSelect');
                select.innerHTML = '<option value="">Sélectionnez un étudiant...</option>';
                window.assignedStudentsList.forEach(student => {
                    const opt = document.createElement('option');
                    opt.value = student.id_assignment; // On se base sur id_assignment
                    opt.textContent = `${student.id_etudiant} - ${student.nom} ${student.prenom}`;
                    select.appendChild(opt);
                });
                document.getElementById('validationStudentDetails').classList.add('hidden');

                if (typeof Chart !== 'undefined') {
                    window.renderEtape3Chart();
                }
            }
        } catch (error) {
            console.error("Erreur chargement des affectations", error);
        }
    };

    window.onValidationStudentChange = function () {
        const select = document.getElementById('validationStudentSelect');
        const id_assignment = select.value;
        const detailsDiv = document.getElementById('validationStudentDetails');

        if (!id_assignment) {
            detailsDiv.classList.add('hidden');
            return;
        }

        const student = window.assignedStudentsList.find(s => s.id_assignment == id_assignment);
        if (student) {
            document.getElementById('vsNom').textContent = `${student.nom} ${student.prenom}`;
            document.getElementById('vsFiliere').textContent = student.nom_filiere;
            document.getElementById('vsUniversity').textContent = student.university_name;

            const badge = document.getElementById('vsStatusBadge');

            const btnAccept = document.getElementById('btnForceAccept');
            const btnDecline = document.getElementById('btnForceDecline');
            const btnPending = document.getElementById('btnForcePending');

            btnAccept.style.display = '';
            btnDecline.style.display = '';
            btnPending.style.display = '';

            if (student.status === 'accepted') {
                badge.textContent = 'Accepté';
                badge.className = 'px-2 py-0.5 rounded text-xs font-bold text-white bg-green-500';
                btnAccept.style.display = 'none';
            } else if (student.status === 'declined') {
                badge.textContent = 'Refusé';
                badge.className = 'px-2 py-0.5 rounded text-xs font-bold text-white bg-red-500';
                btnDecline.style.display = 'none';
            } else {
                badge.textContent = 'En attente';
                badge.className = 'px-2 py-0.5 rounded text-xs font-bold text-white bg-amber-500';
                btnPending.style.display = 'none';
            }

            detailsDiv.classList.remove('hidden');
        }
    };

    window.updateAssignmentStatusExec = async function (id_assignment, new_status) {
        try {
            const payload = {
                id_assignment: parseInt(id_assignment, 10),
                new_status: new_status
            };
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/mobility/update-assignment-status", {
                method: 'POST',
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                alert("Statut mis à jour avec succès.");
                window.fetchAssignedStudents();
                if (typeof refreshAllData === 'function') {
                    refreshAllData();
                }
            } else {
                alert("Erreur lors de la mise à jour.");
            }
        } catch (error) {
            alert("Erreur de connexion.");
        }
    };

    window.updateAssignmentStatusUI = function (new_status) {
        const id_assignment = document.getElementById('validationStudentSelect').value;
        if (!id_assignment) return;

        let actionStr = "";
        if (new_status === 'accepted') actionStr = "l'acceptation";
        else if (new_status === 'declined') actionStr = "le refus";
        else actionStr = "la remise en attente";

        window.requireConfirmation(
            `Vous êtes sur le point de forcer ${actionStr} de cette affectation.`,
            () => window.updateAssignmentStatusExec(id_assignment, new_status)
        );
    };

    window.chartEtape3 = null;

    window.renderEtape3Chart = function () {
        const ctx = document.getElementById('chartEtape3Status');
        if (!ctx) return;

        let countAcc = 0, countPend = 0, countDec = 0;
        window.assignedStudentsList.forEach(s => {
            if (s.status === 'accepted') countAcc++;
            else if (s.status === 'declined') countDec++;
            else countPend++;
        });

        if (window.chartEtape3) {
            window.chartEtape3.destroy();
        }

        window.chartEtape3 = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Acceptés', 'En attente', 'Refusés'],
                datasets: [{
                    data: [countAcc, countPend, countDec],
                    backgroundColor: ['#22c55e', '#f59e0b', '#ef4444'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } }
                }
            },
            plugins: [{
                id: 'textInsideSlices',
                afterDraw: function (chart) {
                    const ctx = chart.ctx;
                    chart.data.datasets.forEach((dataset, i) => {
                        const meta = chart.getDatasetMeta(i);
                        meta.data.forEach((element, index) => {
                            const data = dataset.data[index];
                            if (data > 0) {
                                ctx.save();
                                const centerPoint = element.tooltipPosition();
                                ctx.fillStyle = '#ffffff';
                                ctx.font = 'bold 14px Arial';
                                ctx.textAlign = 'center';
                                ctx.textBaseline = 'middle';
                                // Slight text shadow for better readability
                                ctx.shadowColor = 'rgba(0,0,0,0.5)';
                                ctx.shadowBlur = 4;
                                ctx.fillText(data, centerPoint.x, centerPoint.y);
                                ctx.restore();
                            }
                        });
                    });
                }
            }]
        });
    };

    window.exportAssignedData = async function (status) {
        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/mobility/assigned-students/export/" + status, {
                method: 'GET',
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`
                }
            });
            if (!response.ok) {
                alert("Erreur lors de l'exportation des données.");
                return;
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `Export_Affectations_${status}_${new Date().toISOString().slice(0, 10)}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            alert("Erreur de connexion.");
        }
    };

    // Security Logic for Critical Actions
    let currentActionCallback = null;
    let expectedCode = "";

    window.requireConfirmation = function (description, callback) {
        const modal = document.getElementById('confirmActionModal');
        const descEl = document.getElementById('confirmActionDescription');
        const codeDisplay = document.getElementById('confirmActionCodeDisplay');
        const codeInput = document.getElementById('confirmActionCodeInput');
        const btnConfirm = document.getElementById('confirmActionButton');

        // Generate random 6 character alphanumeric code
        expectedCode = Math.random().toString(36).substring(2, 8).toUpperCase();

        descEl.textContent = description;
        codeDisplay.textContent = expectedCode;
        codeInput.value = "";
        btnConfirm.disabled = true;
        btnConfirm.classList.add('opacity-50', 'cursor-not-allowed');

        currentActionCallback = callback;
        modal.classList.remove('hidden');

        setTimeout(() => codeInput.focus(), 100);
    };

    document.getElementById('confirmActionCodeInput').addEventListener('input', function (e) {
        const val = e.target.value.trim().toUpperCase();
        const btnConfirm = document.getElementById('confirmActionButton');
        if (val === expectedCode) {
            btnConfirm.disabled = false;
            btnConfirm.classList.remove('opacity-50', 'cursor-not-allowed');
        } else {
            btnConfirm.disabled = true;
            btnConfirm.classList.add('opacity-50', 'cursor-not-allowed');
        }
    });

    document.getElementById('confirmActionButton').addEventListener('click', function () {
        if (!document.getElementById('confirmActionButton').disabled && currentActionCallback) {
            document.getElementById('confirmActionModal').classList.add('hidden');
            currentActionCallback();
        }
    });

    window.forceSubmitWishesUI = function () {
        window.requireConfirmation(
            "Vous êtes sur le point de clôturer définitivement toutes les soumissions de vœux. Tous les étudiants ayant fait au moins 1 choix verront leur dossier verrouillé.",
            window.forceSubmitWishesExec
        );
    };

    window.runAssignmentUI = function () {
        window.requireConfirmation(
            "Vous êtes sur le point de lancer l'algorithme d'affectation automatique. Ceci écrase les affectations précédentes non validées.",
            window.runAssignmentExec
        );
    };

    // Diagnostics Logic
    window.exportDiagnosticData = async function (category) {
        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/mobility/diagnostics/export/" + category, {
                method: 'GET',
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`
                }
            });
            if (!response.ok) {
                alert("Erreur lors de l'exportation des données de diagnostique");
                return;
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `Export_Mobilite_Stats_${category}_${new Date().toISOString().slice(0, 10)}.xlsx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            alert("Erreur de connexion.");
        }
    };

    let chartGlobal = null;
    let chartWishes = null;
    let chartDist = null;

    window.toggleDiagnostics = function () {
        const modal = document.getElementById('diagnosticsModal');
        if (modal.classList.contains('hidden')) {
            modal.classList.remove('hidden');
            window.loadDiagnostics();
        } else {
            modal.classList.add('hidden');
        }
    };

    window.loadDiagnostics = async function () {
        try {
            const response = await fetch(window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT + "/university/admin/mobility/diagnostics", {
                method: 'GET',
                headers: {
                    "Authorization": `Bearer ${window.ENV.USER_TOKEN}`
                }
            });

            if (!response.ok) return;

            const data = await response.json();

            if (chartGlobal) chartGlobal.destroy();
            if (chartWishes) chartWishes.destroy();
            if (chartDist) chartDist.destroy();

            // 1. Graphe Global (Pie Chart)
            const ctxGlobal = document.getElementById('chartGlobalStatus').getContext('2d');
            chartGlobal = new Chart(ctxGlobal, {
                type: 'pie',
                data: {
                    labels: ['Mobilités déjà validées', 'Mobilités non validées'],
                    datasets: [{
                        data: [data.validated_mobility, data.remaining_students],
                        backgroundColor: ['#3b82f6', '#9ca3af'], // blue, gray
                        borderWidth: (data.validated_mobility > 0 && data.remaining_students > 0) ? 1 : 0
                    }]
                },
                plugins: [ChartDataLabels],
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } },
                        datalabels: {
                            color: '#ffffff',
                            font: { weight: 'bold', size: 14 },
                            formatter: function (value) {
                                return value > 0 ? value : null;
                            }
                        }
                    }
                }
            });

            // 2. Graphe Avancement (Pie Chart)
            const ctxWishes = document.getElementById('chartWishesStatus').getContext('2d');
            let activeWishesSlices = [data.wishes_submitted, data.wishes_in_progress, data.retardataires].filter(v => v > 0).length;
            chartWishes = new Chart(ctxWishes, {
                type: 'pie',
                data: {
                    labels: ['Vœux soumis', 'En cours (non soumis)', 'Retardataires (0 vœu)'],
                    datasets: [{
                        data: [data.wishes_submitted, data.wishes_in_progress, data.retardataires],
                        backgroundColor: ['#22c55e', '#f59e0b', '#ef4444'], // green, amber, red
                        borderWidth: activeWishesSlices > 1 ? 1 : 0
                    }]
                },
                plugins: [ChartDataLabels],
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } },
                        datalabels: {
                            color: '#ffffff',
                            font: { weight: 'bold', size: 14 },
                            formatter: function (value) {
                                return value > 0 ? value : null;
                            }
                        }
                    }
                }
            });

            // 3. Graphe Distribution (Bar Chart)
            const ctxDist = document.getElementById('chartWishesDistribution').getContext('2d');
            const dist = data.wishes_distribution;
            chartDist = new Chart(ctxDist, {
                type: 'bar',
                data: {
                    labels: ['1 vœu', '2 vœux', '3 vœux', '4 vœux', '5 vœux'],
                    datasets: [{
                        label: 'Nombre d\'étudiants',
                        data: [dist["1"], dist["2"], dist["3"], dist["4"], dist["5"]],
                        backgroundColor: '#6366f1', // indigo
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, ticks: { stepSize: 1 } }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });

        } catch (error) {
            console.error("Erreur lors du chargement des diagnostiques:", error);
        }
    };

    window.closeAssignmentPhase = function () {
        window.requireConfirmation(
            "Cette action va clôturer la phase d'acceptation. TOUTES les affectations actuellement 'en attente' seront définitivement passées à 'refusé'.",
            async function () {
                try {
                    const url = (window.ENV.BACKEND_URL + ':' + window.ENV.BACKEND_PORT) + "/university/admin/mobility/assignment/close";
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${window.ENV.USER_TOKEN}`,
                            'Content-Type': 'application/json'
                        }
                    });
                    if (!response.ok) throw new Error("Erreur lors de la clôture des affectations");

                    alert("Opération terminée avec succès. Toutes les affectations en attente ont été refusées.");

                    // Recharger les données pour rafraîchir l'interface
                    window.fetchStatsAndPopulate();
                    fetchAssignmentsForValidation();

                } catch (error) {
                    console.error(error);
                    alert("Erreur: " + error.message);
                }
            }
        );
    };

</script>
<?php $t->endSlot(); ?>