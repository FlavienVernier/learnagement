document.addEventListener("DOMContentLoaded", () => {
    // Shared elements
    const btnPrev = document.getElementById("btn_prev");
    const btnNext = document.getElementById("btn_next");
    const pageInfo = document.getElementById("page_info");

    // Add CSS animation for fade in if not present
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);

    // =========================================================
    // LOGIQUE ENSEIGNANTS
    // =========================================================
    const profs = Array.from(document.querySelectorAll(".enseignant"));
    if (profs.length > 0) {
        // Configuration
        const itemsPerPage = 12;
        let currentPage = 1;
        const totalPages = Math.ceil(profs.length / itemsPerPage) || 1;

        function showProfPage(page) {
            // Validation
            if (page < 1) page = 1;
            if (page > totalPages) page = totalPages;
            currentPage = page;

            // Calculate start and end indices
            const start = (currentPage - 1) * itemsPerPage;
            const end = start + itemsPerPage;

            // Toggle visibility
            profs.forEach((prof, index) => {
                if (index >= start && index < end) {
                    prof.style.display = "flex";
                    prof.style.opacity = "0";
                    prof.style.animation = "fadeIn 0.3s forwards";
                } else {
                    prof.style.display = "none";
                }
            });

            // Update UI
            if (pageInfo) pageInfo.textContent = `Page ${currentPage} sur ${totalPages}`;

            // Update buttons state
            if (btnPrev) btnPrev.disabled = (currentPage === 1);
            if (btnNext) btnNext.disabled = (currentPage === totalPages);
        }

        // Event Listeners
        if (btnPrev) {
            btnPrev.addEventListener("click", () => {
                if (currentPage > 1) showProfPage(currentPage - 1);
            });
        }
        if (btnNext) {
            btnNext.addEventListener("click", () => {
                if (currentPage < totalPages) showProfPage(currentPage + 1);
            });
        }

        // Initialize
        showProfPage(1);
        return; // Exit as we are in teacher mode
    }

    // =========================================================
    // LOGIQUE ETUDIANTS
    // =========================================================
    const etudiants = Array.from(document.querySelectorAll('.etudiant'));
    if (etudiants.length > 0) {
        const searchInput = document.getElementById('search_input');
        const btnRecherche = document.getElementById('btn_recherche');
        const filtresActifs = document.getElementById('filtres_actifs');

        let filtres = [];
        const parPage = 12;
        let pageCourante = 1;
        let filteredEtudiants = [...etudiants];

        // Ajouter un filtre
        function ajouterFiltre(texte) {
            if (filtres.includes(texte.toLowerCase()) || texte.trim() === '') return;
            // (\D+) = capture tout ce qui n'est pas un chiffre
            // (\d+) = capture les chiffres
            texte = texte.replace(/\s+/g, '');
            const resultat1 = texte.match(/(\D+)(\d+)/);
            const resultat2 = texte.match(/(\d+)(\D+)/);
            if (!resultat1 && !resultat2) {
                filtres.push(texte.toLowerCase());
            }
            else {
                const filtreTexte = resultat1 ? resultat1[1] : resultat2[2];
                const filtreChiffre = resultat1 ? resultat1[2] : resultat2[1];
                filtres.push(filtreTexte.toLowerCase());
                filtres.push(filtreChiffre);
            }
            afficherFiltres();
            appliquerFiltres();
            if (searchInput) searchInput.value = '';
        }

        // Supprimer un filtre
        function supprimerFiltre(texte) {
            filtres = filtres.filter(f => f !== texte);
            afficherFiltres();
            appliquerFiltres();
        }

        // Afficher les tags de filtres
        function afficherFiltres() {
            if (!filtresActifs) return;
            filtresActifs.innerHTML = '';
            filtres.forEach(filtre => {
                const tag = document.createElement('div');
                tag.className = 'filtre_tag';
                tag.innerHTML = `<span>${filtre}</span> <button class="btn_remove" data-filtre="${filtre}"></button>`;
                filtresActifs.appendChild(tag);
            });

            document.querySelectorAll('.btn_remove').forEach(btn => {
                btn.addEventListener('click', function () {
                    supprimerFiltre(this.dataset.filtre);
                });
            });
        }

        // Appliquer les filtres
        function appliquerFiltres() {
            if (filtres.length === 0) {
                filteredEtudiants = [...etudiants];
            } else {
                filteredEtudiants = etudiants.filter(etudiant => {
                    let texteNomPrenom = "";
                    let texteFiliere = "";

                    if (etudiant.children.length >= 2) {
                        texteNomPrenom = etudiant.children[0].textContent.toLowerCase();
                        texteFiliere = etudiant.children[1].textContent.toLowerCase();
                    } else {
                        texteNomPrenom = etudiant.textContent.toLowerCase();
                    }

                    return filtres.every(filtre =>
                        texteNomPrenom.includes(filtre) || texteFiliere.includes(filtre)
                    );
                });
            }

            pageCourante = 1;
            afficherEtuPage(1);
        }

        // Pagination Etudiants
        function afficherEtuPage(numPage) {
            etudiants.forEach(e => e.style.display = "none");
            const dynamicTotalPages = Math.ceil(filteredEtudiants.length / parPage) || 1;
            const debut = (numPage - 1) * parPage;
            const fin = debut + parPage;

            for (let i = debut; i < fin && i < filteredEtudiants.length; i++) {
                filteredEtudiants[i].style.visibility = "visible";
                filteredEtudiants[i].style.display = "flex";
                filteredEtudiants[i].style.animation = "fadeIn 0.3s forwards";
            }

            if (btnPrev) btnPrev.disabled = (numPage === 1);
            if (btnNext) btnNext.disabled = (numPage >= dynamicTotalPages);
            if (pageInfo) pageInfo.textContent = `Page ${numPage} sur ${dynamicTotalPages}`;
        }

        // Event Listeners Etudiants
        if (btnRecherche) {
            btnRecherche.addEventListener('click', () => ajouterFiltre(searchInput.value));
        }
        if (searchInput) {
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    ajouterFiltre(searchInput.value);
                }
            });
        }
        if (btnPrev) {
            btnPrev.addEventListener('click', () => {
                const dynamicTotalPages = Math.ceil(filteredEtudiants.length / parPage) || 1;
                if (pageCourante > 1) {
                    pageCourante--;
                    afficherEtuPage(pageCourante);
                }
            });
        }
        if (btnNext) {
            btnNext.addEventListener('click', () => {
                const dynamicTotalPages = Math.ceil(filteredEtudiants.length / parPage) || 1;
                if (pageCourante < dynamicTotalPages) {
                    pageCourante++;
                    afficherEtuPage(pageCourante);
                }
            });
        }

        // Init
        afficherEtuPage(1);
    }
});
