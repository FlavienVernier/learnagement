<?php $t->extend('layouts/dashboard'); ?>

<?php $t->startSlot('title'); ?>Ressources — Learnagement<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>
    <!-- En-tête -->
    <div class="mb-8">
        <h1 class="text-2xl font-medium text-[#0f2744] mb-1">Ressources universitaires</h1>
        <p class="text-sm text-slate-500">Services et dispositifs mis à disposition des étudiants de l'USMB</p>
    </div>

    <!-- Grille de cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

        <!-- SERVICE DES SPORTS -->
        <div class="bg-white border border-black/8 rounded-xl p-5">
            <div class="flex items-start gap-3 mb-3">
                <div class="w-9 h-9 rounded-lg bg-blue-50 flex items-center justify-center shrink-0">
                    <svg width="18" height="18" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="#1b6ca8" stroke-width="1.8"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" stroke="#1b6ca8" stroke-width="1.8"/><path d="M2 12h20" stroke="#1b6ca8" stroke-width="1.8"/></svg>
                </div>
                <div>
                    <h2 class="text-sm font-medium text-[#0f2744]">Service des sports</h2>
                    <a href="https://www.univ-smb.fr/espace-etudiant/vie-etudiante/sport/" target="_blank"
                    class="text-xs text-blue-600 hover:underline">univ-smb.fr →</a>
                </div>
            </div>
            <p class="text-sm text-slate-600 leading-relaxed mb-3">
                Inscription gratuite à un sport chaque semestre. Chaque sport supplémentaire est facturé 15€.
            </p>
            <a href="https://www.univ-smb.fr/espace-etudiant/vie-etudiante/sport/" target="_blank"
            class="inline-flex items-center gap-1.5 text-xs font-medium text-blue-700 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-lg transition-colors">
                <svg width="12" height="12" fill="none" viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                Accéder au service
            </a>
        </div>

        <!-- BIBLIOTHÈQUE -->
        <div class="bg-white border border-black/8 rounded-xl p-5">
            <div class="flex items-start gap-3 mb-3">
                <div class="w-9 h-9 rounded-lg bg-indigo-50 flex items-center justify-center shrink-0">
                    <svg width="18" height="18" fill="none" viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" stroke="#4f46e5" stroke-width="1.8"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" stroke="#4f46e5" stroke-width="1.8"/></svg>
                </div>
                <div>
                    <h2 class="text-sm font-medium text-[#0f2744]">Bibliothèque universitaire</h2>
                    <a href="https://www.univ-smb.fr/espace-etudiant/vie-etudiante/bibliotheques/" target="_blank"
                    class="text-xs text-blue-600 hover:underline">univ-smb.fr →</a>
                </div>
            </div>
            <p class="text-sm text-slate-600 leading-relaxed mb-3">
                Documents empruntables, espaces de travail, ordinateurs, imprimantes, scanners et tableaux blancs disponibles.
            </p>
            <div class="bg-slate-50 border border-black/5 rounded-lg px-3 py-2.5 mb-3 flex items-center gap-2">
                <svg width="14" height="14" fill="none" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" stroke="#64748b" stroke-width="1.8"/><line x1="3" y1="10" x2="21" y2="10" stroke="#64748b" stroke-width="1.8"/></svg>
                <span class="text-xs text-slate-600">Réservation de salles (1–10 personnes · 2h/jour)</span>
            </div>
            <a href="https://www.univ-smb.fr/bu/services/reserver-une-salle-de-travail/" target="_blank"
            class="inline-flex items-center gap-1.5 text-xs font-medium text-indigo-700 bg-indigo-50 hover:bg-indigo-100 px-3 py-1.5 rounded-lg transition-colors">
                <svg width="12" height="12" fill="none" viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                Réserver une salle
            </a>
        </div>

        <!-- SANTÉ -->
        <div class="bg-white border border-black/8 rounded-xl p-5">
            <div class="flex items-start gap-3 mb-4">
                <div class="w-9 h-9 rounded-lg bg-red-50 flex items-center justify-center shrink-0">
                    <svg width="18" height="18" fill="none" viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2" stroke="#dc2626" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
                <div>
                    <h2 class="text-sm font-medium text-[#0f2744]">Santé et accompagnement</h2>
                    <p class="text-xs text-slate-400">Aménagements, signalement, soutien</p>
                </div>
            </div>

            <div class="space-y-3">
                <div class="border border-black/5 rounded-lg p-3">
                    <p class="text-xs font-medium text-[#0f2744] mb-1">Aménagements d'études</p>
                    <p class="text-xs text-slate-500 leading-relaxed mb-2">
                        Dispositifs adaptés aux situations personnelles pour favoriser la réussite universitaire.
                    </p>
                    <a href="https://www.univ-smb.fr/espace-etudiant/etudes/amenagements-detudes/" target="_blank"
                    class="text-xs text-blue-600 hover:underline">Consulter les aménagements →</a>
                </div>

                <div class="border border-black/5 rounded-lg p-3">
                    <p class="text-xs font-medium text-[#0f2744] mb-1">Lutte contre les violences</p>
                    <p class="text-xs text-slate-500 leading-relaxed mb-2">
                        Plateforme sécurisée et confidentielle pour signaler toute situation de violence, harcèlement ou discrimination.
                    </p>
                    <div class="flex flex-col gap-1">
                        <a href="https://www.univ-smb.fr/espace-etudiant/aides-et-soutiens/plateforme-de-signalement/" target="_blank"
                        class="text-xs text-blue-600 hover:underline">Plateforme de signalement →</a>
                        <a href="https://www.univ-smb.fr/espace-etudiant/vie-etudiante/egalite-et-lutte-contre-les-discriminations/" target="_blank"
                        class="text-xs text-blue-600 hover:underline">Égalité et lutte contre les discriminations →</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- VIE ASSOCIATIVE -->
        <div class="bg-white border border-black/8 rounded-xl p-5">
            <div class="flex items-start gap-3 mb-3">
                <div class="w-9 h-9 rounded-lg bg-green-50 flex items-center justify-center shrink-0">
                    <svg width="18" height="18" fill="none" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="#16a34a" stroke-width="1.8"/><circle cx="9" cy="7" r="4" stroke="#16a34a" stroke-width="1.8"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round"/></svg>
                </div>
                <div>
                    <h2 class="text-sm font-medium text-[#0f2744]">Vie associative</h2>
                    <a href="https://www.univ-smb.fr/espace-etudiant/vie-etudiante/vie-associative/" target="_blank"
                    class="text-xs text-blue-600 hover:underline">univ-smb.fr →</a>
                </div>
            </div>
            <p class="text-sm text-slate-600 leading-relaxed mb-3">
                Plus de 50 associations labellisées animent la vie étudiante sur les campus. Le SVEC accompagne les étudiants souhaitant créer ou rejoindre une association.
            </p>
            <div class="flex gap-2 flex-wrap">
                <a href="https://www.univ-smb.fr/espace-etudiant/vie-etudiante/vie-associative/" target="_blank"
                class="inline-flex items-center gap-1.5 text-xs font-medium text-green-700 bg-green-50 hover:bg-green-100 px-3 py-1.5 rounded-lg transition-colors">
                    <svg width="12" height="12" fill="none" viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    Voir les associations
                </a>
                <a href="https://www.univ-smb.fr/espace-etudiant/bienvenue-a-lusmb/etudes/#svec" target="_blank"
                class="inline-flex items-center gap-1.5 text-xs font-medium text-slate-600 bg-slate-50 hover:bg-slate-100 px-3 py-1.5 rounded-lg transition-colors">
                    Découvrir le SVEC
                </a>
            </div>
        </div>

        <!-- RESSOURCES NUMÉRIQUES — pleine largeur -->
        <div class="bg-white border border-black/8 rounded-xl p-5 md:col-span-2">
            <div class="flex items-start justify-between gap-4">
                <div class="flex items-start gap-3">
                    <div class="w-9 h-9 rounded-lg bg-purple-50 flex items-center justify-center shrink-0">
                        <svg width="18" height="18" fill="none" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" stroke="#9333ea" stroke-width="1.8"/><line x1="8" y1="21" x2="16" y2="21" stroke="#9333ea" stroke-width="1.8" stroke-linecap="round"/><line x1="12" y1="17" x2="12" y2="21" stroke="#9333ea" stroke-width="1.8" stroke-linecap="round"/></svg>
                    </div>
                    <div>
                        <h2 class="text-sm font-medium text-[#0f2744]">Ressources informatiques</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Intranet · Mail universitaire · Logiciels · Wifi Eduroam</p>
                    </div>
                </div>
                <a href="https://www.univ-smb.fr/espace-etudiant/bienvenue-a-lusmb/les-outils-numeriques/" target="_blank"
                class="inline-flex items-center gap-1.5 text-xs font-medium text-purple-700 bg-purple-50 hover:bg-purple-100 px-3 py-1.5 rounded-lg transition-colors shrink-0">
                    <svg width="12" height="12" fill="none" viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    Accéder aux outils
                </a>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
                <div class="bg-slate-50 rounded-lg px-3 py-2.5 text-center">
                    <svg class="mx-auto mb-1" width="16" height="16" fill="none" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" stroke="#64748b" stroke-width="1.8"/><line x1="8" y1="21" x2="16" y2="21" stroke="#64748b" stroke-width="1.8" stroke-linecap="round"/></svg>
                    <p class="text-xs text-slate-600">Intranet</p>
                </div>
                <div class="bg-slate-50 rounded-lg px-3 py-2.5 text-center">
                    <svg class="mx-auto mb-1" width="16" height="16" fill="none" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="#64748b" stroke-width="1.8"/><polyline points="22,6 12,13 2,6" stroke="#64748b" stroke-width="1.8"/></svg>
                    <p class="text-xs text-slate-600">Mail universitaire</p>
                </div>
                <div class="bg-slate-50 rounded-lg px-3 py-2.5 text-center">
                    <svg class="mx-auto mb-1" width="16" height="16" fill="none" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" stroke="#64748b" stroke-width="1.8"/><line x1="3" y1="10" x2="21" y2="10" stroke="#64748b" stroke-width="1.8"/></svg>
                    <p class="text-xs text-slate-600">Logiciels gratuits</p>
                </div>
                <div class="bg-slate-50 rounded-lg px-3 py-2.5 text-center">
                    <svg class="mx-auto mb-1" width="16" height="16" fill="none" viewBox="0 0 24 24"><path d="M5 12.55a11 11 0 0 1 14.08 0M1.42 9a16 16 0 0 1 21.16 0M8.53 16.11a6 6 0 0 1 6.95 0M12 20h.01" stroke="#64748b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    <p class="text-xs text-slate-600">Wifi Eduroam</p>
                </div>
            </div>
        </div>

    </div>
<?php $t->endSlot(); ?>