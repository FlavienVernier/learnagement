<?php $t->extend('layouts/base'); ?>

<?php $t->startSlot('title'); ?>Page d'accueil — Learnagement<?php $t->endSlot(); ?>

<?php $t->startSlot('content'); ?>
<!-- Hero -->
<section class="px-8 pt-16 pb-14 text-center bg-primary">
    <div class="inline-flex items-center gap-2 bg-blue-600/20 border border-blue-500/40 text-blue-300 text-xs px-4 py-1.5 rounded-full mb-6">
        <span class="w-1.5 h-1.5 bg-blue-400 rounded-full"></span>
        École d'ingénieurs publique · USMB
    </div>
    <h1 class="text-white text-4xl font-medium leading-tight mb-4 max-w-xl mx-auto">
        Toutes vos infos <span class="text-blue-400">Polytech</span> au même endroit
    </h1>
    <p class="text-white/60 text-sm leading-relaxed max-w-md mx-auto mb-8">
        Learnagement centralise les ressources pédagogiques, documents administratifs et actualités pour les étudiants et personnels de Polytech Annecy-Chambéry.
    </p>
    <div class="flex gap-3 justify-center flex-wrap">
        <a href="<?= $t->router->href('login') ?>" class="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-7 py-3 rounded-xl transition-colors">
            Accéder à mon espace
        </a>
        <a href="https://www.univ-smb.fr/polytech/" class="bg-white/8 hover:bg-white/14 text-white/85 border border-white/20 text-sm px-7 py-3 rounded-xl transition-colors">
            Découvrir l'école
        </a>
    </div>
</section>

<!-- Stats -->
<div class="flex justify-center bg-primary border-t border-b border-white/8">
    <div class="flex divide-x divide-white/8">
        <div class="px-10 py-6 text-center">
            <div class="text-white text-2xl font-medium">5</div>
            <div class="text-white/45 text-xs mt-1">Formations ingénieur</div>
        </div>
        <div class="px-10 py-6 text-center">
            <div class="text-white text-2xl font-medium">900+</div>
            <div class="text-white/45 text-xs mt-1">Étudiants</div>
        </div>
        <div class="px-10 py-6 text-center">
            <div class="text-white text-2xl font-medium">30+</div>
            <div class="text-white/45 text-xs mt-1">Ans d'existence</div>
        </div>
        <div class="px-10 py-6 text-center">
            <div class="text-white text-2xl font-medium">3</div>
            <div class="text-white/45 text-xs mt-1">Laboratoires de recherche</div>
        </div>
    </div>
</div>

<!-- Features -->
<section class="bg-gray-50 px-8 py-14">
    <div class="max-w-5xl mx-auto">
        <div class="text-center mb-9">
            <h2 class="text-[#0f2744] text-xl font-medium mb-2">Tout ce dont vous avez besoin</h2>
            <p class="text-slate-500 text-sm">Un portail unique pour les étudiants, enseignants et personnels administratifs.</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

            <div class="bg-white border border-black/8 rounded-xl p-5">
                <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center mb-4">
                    <svg width="20" height="20" fill="none" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" stroke="#1b6ca8" stroke-width="1.8"/><line x1="16" y1="2" x2="16" y2="6" stroke="#1b6ca8" stroke-width="1.8" stroke-linecap="round"/><line x1="8" y1="2" x2="8" y2="6" stroke="#1b6ca8" stroke-width="1.8" stroke-linecap="round"/><line x1="3" y1="10" x2="21" y2="10" stroke="#1b6ca8" stroke-width="1.8"/></svg>
                </div>
                <h3 class="text-[#0f2744] text-sm font-medium mb-1.5">Planning & emploi du temps</h3>
                <p class="text-slate-500 text-xs leading-relaxed">Consultez votre EDT en temps réel, recevez des alertes de modifications et synchronisez avec votre agenda.</p>
            </div>

            <div class="bg-white border border-black/8 rounded-xl p-5">
                <div class="w-10 h-10 bg-green-50 rounded-lg flex items-center justify-center mb-4">
                    <svg width="20" height="20" fill="none" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
                </div>
                <h3 class="text-[#0f2744] text-sm font-medium mb-1.5">Notes & résultats</h3>
                <p class="text-slate-500 text-xs leading-relaxed">Accédez à vos notes, moyennes et relevés de notes par semestre. Suivez votre progression tout au long de l'année.</p>
            </div>

            <div class="bg-white border border-black/8 rounded-xl p-5">
                <div class="w-10 h-10 bg-amber-50 rounded-lg flex items-center justify-center mb-4">
                    <svg width="20" height="20" fill="none" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="#d97706" stroke-width="1.8"/><polyline points="14 2 14 8 20 8" stroke="#d97706" stroke-width="1.8"/></svg>
                </div>
                <h3 class="text-[#0f2744] text-sm font-medium mb-1.5">Documents administratifs</h3>
                <p class="text-slate-500 text-xs leading-relaxed">Téléchargez vos certificats de scolarité, déposez vos justificatifs et gérez vos conventions de stage.</p>
            </div>

            <div class="bg-white border border-black/8 rounded-xl p-5">
                <div class="w-10 h-10 bg-purple-50 rounded-lg flex items-center justify-center mb-4">
                    <svg width="20" height="20" fill="none" viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" stroke="#9333ea" stroke-width="1.8"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" stroke="#9333ea" stroke-width="1.8"/></svg>
                </div>
                <h3 class="text-[#0f2744] text-sm font-medium mb-1.5">Ressources pédagogiques</h3>
                <p class="text-slate-500 text-xs leading-relaxed">Retrouvez les supports de cours, annales et documents partagés par vos enseignants en un seul endroit.</p>
            </div>

            <div class="bg-white border border-black/8 rounded-xl p-5">
                <div class="w-10 h-10 bg-rose-50 rounded-lg flex items-center justify-center mb-4">
                    <svg width="20" height="20" fill="none" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="#e11d48" stroke-width="1.8"/></svg>
                </div>
                <h3 class="text-[#0f2744] text-sm font-medium mb-1.5">Messagerie interne</h3>
                <p class="text-slate-500 text-xs leading-relaxed">Échangez directement avec vos enseignants, votre responsable de formation et les services administratifs.</p>
            </div>

            <div class="bg-white border border-black/8 rounded-xl p-5">
                <div class="w-10 h-10 bg-teal-50 rounded-lg flex items-center justify-center mb-4">
                    <svg width="20" height="20" fill="none" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="#0f6e56" stroke-width="1.8"/><path d="M12 6v6l4 2" stroke="#0f6e56" stroke-width="1.8" stroke-linecap="round"/></svg>
                </div>
                <h3 class="text-[#0f2744] text-sm font-medium mb-1.5">Actualités & événements</h3>
                <p class="text-slate-500 text-xs leading-relaxed">Restez informé des news de l'école, des événements BDE et des opportunités professionnelles.</p>
            </div>

        </div>
    </div>
</section>

<!-- Formations -->
<section class="bg-white px-8 py-14">
    <div class="max-w-3xl mx-auto">
        <div class="text-center mb-8">
            <h2 class="text-[#0f2744] text-xl font-medium mb-2">Nos 5 formations ingénieur</h2>
            <p class="text-slate-500 text-sm">Des cursus pour relever les défis des transitions numérique, énergétique et socio-écologique.</p>
        </div>
        <div class="flex flex-col gap-3">

            <div class="flex items-center gap-4 px-5 py-4 border border-black/8 rounded-xl hover:border-blue-500 hover:bg-blue-50/50 transition-colors cursor-pointer">
                <div class="w-1 h-10 bg-blue-600 rounded-full shrink-0"></div>
                <div>
                    <h4 class="text-[#0f2744] text-sm font-medium mb-0.5">Informatique Données Usages</h4>
                    <p class="text-slate-500 text-xs">Data science, développement logiciel, intelligence artificielle</p>
                </div>
                <span class="ml-auto text-xs font-medium px-3 py-1 rounded-full bg-blue-50 text-blue-800 shrink-0">IDU</span>
            </div>

            <div class="flex items-center gap-4 px-5 py-4 border border-black/8 rounded-xl hover:border-green-500 hover:bg-green-50/50 transition-colors cursor-pointer">
                <div class="w-1 h-10 bg-green-600 rounded-full shrink-0"></div>
                <div>
                    <h4 class="text-[#0f2744] text-sm font-medium mb-0.5">Bâtiment Écoconstruction Énergie</h4>
                    <p class="text-slate-500 text-xs">Construction durable, efficacité énergétique, bâtiment intelligent</p>
                </div>
                <span class="ml-auto text-xs font-medium px-3 py-1 rounded-full bg-green-50 text-green-800 shrink-0">BEE</span>
            </div>

            <div class="flex items-center gap-4 px-5 py-4 border border-black/8 rounded-xl hover:border-teal-500 hover:bg-teal-50/50 transition-colors cursor-pointer">
                <div class="w-1 h-10 bg-teal-700 rounded-full shrink-0"></div>
                <div>
                    <h4 class="text-[#0f2744] text-sm font-medium mb-0.5">Écologie Industrielle et Territoriale</h4>
                    <p class="text-slate-500 text-xs">Transition écologique, gestion des ressources, territoires durables</p>
                </div>
                <span class="ml-auto text-xs font-medium px-3 py-1 rounded-full bg-teal-50 text-teal-800 shrink-0">EIT</span>
            </div>

            <div class="flex items-center gap-4 px-5 py-4 border border-black/8 rounded-xl hover:border-amber-500 hover:bg-amber-50/50 transition-colors cursor-pointer">
                <div class="w-1 h-10 bg-amber-500 rounded-full shrink-0"></div>
                <div>
                    <h4 class="text-[#0f2744] text-sm font-medium mb-0.5">Mécanique Mécatronique Matériaux</h4>
                    <p class="text-slate-500 text-xs">Conception mécanique, matériaux composites, mécatronique</p>
                </div>
                <span class="ml-auto text-xs font-medium px-3 py-1 rounded-full bg-amber-50 text-amber-800 shrink-0">3M</span>
            </div>

            <div class="flex items-center gap-4 px-5 py-4 border border-black/8 rounded-xl hover:border-purple-500 hover:bg-purple-50/50 transition-colors cursor-pointer">
                <div class="w-1 h-10 bg-purple-600 rounded-full shrink-0"></div>
                <div>
                    <h4 class="text-[#0f2744] text-sm font-medium mb-0.5">Systèmes Embarqués Automatisation</h4>
                    <p class="text-slate-500 text-xs">Électronique, systèmes temps réel, robotique, capteurs</p>
                </div>
                <span class="ml-auto text-xs font-medium px-3 py-1 rounded-full bg-purple-50 text-purple-800 shrink-0">SEA</span>
            </div>

        </div>
    </div>
</section>

<?php $t->endSlot(); ?>