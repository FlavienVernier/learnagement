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
            <article class="block rounded-2xl p-5 border border-gray-200 dark:border-gray-700 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Dossiers soumis</span>
                    <span class="bg-blue-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                    </span>
                </div>
                <div id="kpiStudents" class="text-4xl font-extrabold text-gray-900">0</div>
                <div class="mt-1 text-xs">Étudiants ayant validé leurs voeux</div>
            </article>

            <article class="block rounded-2xl p-5 border border-gray-200 dark:border-gray-700 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Dossiers incomplets</span>
                    <span class="bg-indigo-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                    </span>
                </div>
                <div id="kpiIncomplete" class="text-4xl font-extrabold text-indigo-600">0</div>
                <div class="mt-1 text-xs">Dossiers non encore soumis</div>
            </article>

            <article class="block rounded-2xl p-5 border border-gray-200 dark:border-gray-700 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Universites ciblées</span>
                    <span class="bg-green-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5l9-3 9 3-9 3-9-3zm0 7l9 3 9-3m-18 7l9 3 9-3"/></svg>
                    </span>
                </div>
                <div id="kpiUniversities" class="text-4xl font-extrabold text-green-600">0</div>
                <div class="mt-1 text-xs">Destinations distinctes demandées</div>
            </article>

            <article class="block rounded-2xl p-5 border border-gray-200 dark:border-gray-700 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-medium text-gray-600">Dépots récents</span>
                    <span class="bg-yellow-100 p-2 rounded-lg">
                        <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
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
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                    </div>
                    <input id="wishesSearch" type="search"
                        placeholder="Rechercher un etudiant, email ou universite..."
                        class="border text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 p-2.5"/>
                </div>
                <div class="flex flex-wrap items-center gap-3">
                    <label for="dossierStatusFilter" class="text-xs font-semibold uppercase tracking-wide text-gray-500">Filtre dossier</label>
                    <select id="dossierStatusFilter" class="border border-gray-300 rounded-lg px-3 py-2 text-sm">
                        <option value="tous">Tous</option>
                        <option value="complet">Complet</option>
                        <option value="incomplet">Incomplet</option>
                        <option value="recent">Recent (7 jours)</option>
                    </select>
                    <button id="resetDashboardFilters" type="button" class="inline-flex items-center gap-1.5 px-3 py-2 text-xs font-medium rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 transition">
                        Reinitialiser
                    </button>
                    <span id="wishesResultsCount" class="text-sm">0 resultat</span>
                </div>
            </div>
        </div>

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
                <button onclick="document.getElementById('filterForm').classList.toggle('hidden')" class="bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow text-sm">
                    Filtres carte
                </button>
            </div>

            <form id="filterForm" onsubmit="return false;" class="hidden bg-white p-4 rounded-lg shadow-lg border border-gray-200">
                <div class="flex flex-wrap justify-center items-center gap-4">
                    <div class="flex flex-col">
                        <label for="semestreSelect" class="text-xs font-semibold text-gray-600 mb-1">Semestre</label>
                        <select name="semestre" id="semestreSelect" onchange="updateMap()" class="border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary min-w-24">
                            <option value="Tous">Tous</option>
                            <option value="S8">S8</option>
                            <option value="S9">S9</option>
                        </select>
                    </div>
                    <div class="flex flex-col">
                        <label for="filiereSelect" class="text-xs font-semibold text-gray-600 mb-1">Filiere</label>
                        <select name="filiere" id="filiereSelect" onchange="updateMap()" class="border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:border-primary min-w-48">
                            <option value="toutes">Toutes</option>
                        </select>
                    </div>
                    <div class="flex flex-col">
                        <div class="flex justify-between items-center mb-1">
                            <label for="noteMinRange" class="text-xs font-semibold text-gray-600">Note minimale</label>
                            <span id="noteMinValue" class="text-xs font-bold text-gray-700">20</span>
                        </div>
                        <input type="range" name="notemin" id="noteMinRange" min="0" max="20" value="20" class="w-32 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary" oninput="document.getElementById('noteMinValue').innerText = this.value; updateMap()">
                    </div>
                </div>
            </form>
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
</section>
<?php $t->endSlot(); ?>


<?php $t->startSlot('style.top'); ?>
<!-- Import Leaflet CSS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
crossorigin=""/>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
<link rel="stylesheet" href="/APP_2026/theme/mobility-map.css" />
<?php $t->endSlot(); ?>


<?php $t->startSlot('script.top'); ?>
<?php
    $googleMapsApiKey = getenv('GOOGLE_MAPS_API_KEY') ?: ($_ENV['GOOGLE_MAPS_API_KEY'] ?? '');
?>
<!-- Import Leaflet JS -->
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin="">
</script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>

<!-- Google Maps API pour Street View interactif -->
<script src="https://maps.googleapis.com/maps/api/js?key=<?= urlencode($googleMapsApiKey) ?>&libraries=places"></script>

<!-- Logic map dédiée -->
<script src="/APP_2026/theme/mobility-map-carousel.js"></script>
<script src="/APP_2026/theme/mobility-map-streetview.js"></script>

<!-- ToDo : Déplacer dans un fichier global ex db.js -->
<script>
    window.ENV = {
        BACKEND_URL: "http://127.0.0.1",
        BACKEND_PORT: "44000",
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
    const popupState = new Map();
    const wishesCountByUniversityId = new Map();
    window.MobilityMapState = {
        popupState,
        submittedWishesByStudent,
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

            universities = await response.json();
        } catch (error) {
            console.error(error.message);
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

    const universityCatalog = await fetchUniversityCatalog();
    const universitiesById = new Map();
    const filieresById = new Map();

    for (const row of universityCatalog) {
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

    window.MobilityMapState.universitiesById = universitiesById;
    window.MobilityMapState.filieresById = filieresById;

    const filiereSelect = document.getElementById('filiereSelect');
    filiereSelect.innerHTML = '<option value="toutes">Toutes</option>' + Array.from(filieresById.values())
        .sort((a, b) => String(a.nom_filiere).localeCompare(String(b.nom_filiere)))
        .map((filiere) => `<option value="${escapeHtml(String(filiere.id_filiere))}">${escapeHtml(filiere.nom_filiere || filiere.nom_long || 'Filiere')}</option>`)
        .join('');

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
    await refreshWishesFromServer();

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
            const isSubmitted = Boolean(entry.student.submission_date);
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

    window.toggleWishDetails = function(studentId) {
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
                    row.firstWishName,
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

    

    window.flyToUniversity = function(uid) {
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

    window.scrollToUniversityOnMap = function(uid) {
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

        const filtered = universities.filter(u => {
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

    refreshKpis();
    renderDashboardTable();
    updateMap();
</script>
<?php $t->endSlot(); ?>