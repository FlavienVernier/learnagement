const activeFilters = {};
let myGantt = null;

console.log("token", token);
console.log("id utilisateur", userId);
console.log("Données pour le Gantt :", dataGantt);


function getNextSemestre(semestre) {
    if (!semestre) return "S1";
    const num = parseInt(semestre.replace('S', ''));
    return `S${num + 1}`;
}

function formatDate(dateObj) {
    const y = dateObj.getFullYear();
    const m = String(dateObj.getMonth() + 1).padStart(2, '0');
    const d = String(dateObj.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

// Vue Enseignant : On regroupe tout sur une seule année académique (2024-2025)
function semesterToDateEnseignant(semestre) {
    if (!semestre) return { start: "2024-09-01", end: "2025-06-30" };
    const num = parseInt(semestre.replace('S', ''));
    
    if (num % 2 !== 0) {
        return { start: "2024-09-01", end: "2025-01-15" };
    }
    else {
        return { start: "2025-01-20", end: "2025-06-30" };
    }
}
function semesterToDateEtudiant(semestre) {
    const semestreMap = {
        "S1": { start: "2023-09-01", end: "2024-01-15" },
        "S2": { start: "2024-01-20", end: "2024-06-30" },
        "S3": { start: "2024-09-01", end: "2025-01-15" },
        "S4": { start: "2025-01-20", end: "2025-06-30" },
        "S5": { start: "2025-09-01", end: "2026-01-15" },
        "S6": { start: "2026-01-20", end: "2026-06-30" },
        "S7": { start: "2026-09-01", end: "2027-01-15" },
        "S8": { start: "2027-01-20", end: "2027-06-30" },
        "S9": { start: "2027-09-01", end: "2028-01-15" },
        "S10": { start: "2028-01-20", end: "2028-06-30" }
    };
    return semestreMap[semestre] || { start: "2024-01-01", end: "2024-06-01" };
}

function transformDataForDHTMLX(dataGantt, userType) {
    const tasksMap = new Map();
    const links = [];
    let linkIdCounter = 1;

    // Durée par défaut courte pour éviter que les blocs prennent tout le semestre
    const DEFAULT_DURATION_DAYS = 14; 

    // Création des liens 
    dataGantt.forEach(item => {
            const prvKey = `${item.prv_code_module}_${item.prv_type}`;
            const nxtKey = `${item.nxt_code_module}_${item.nxt_type}`;
        if (!tasksMap.has(prvKey)) {
            const dates = userType === 'enseignant'
                ? semesterToDateEnseignant(item.prv_semestre)
                : semesterToDateEtudiant(item.prv_semestre);

            tasksMap.set(prvKey, {
                id: prvKey,
                text: prvKey,
                start_date: dates.start, 
                duration: item.prv_duree_h ? Math.ceil(item.prv_duree_h / 2) : DEFAULT_DURATION_DAYS,
                code_module: item.prv_code_module, 
                duree_h: item.prv_duree_h,
                type: item.prv_type
            });
        }

        // Enfant
        const nxtSemestre = item.nxt_semestre || getNextSemestre(item.prv_semestre);
        if (!tasksMap.has(nxtKey)) {
            const dates = userType === 'enseignant'
                ? semesterToDateEnseignant(nxtSemestre)
                : semesterToDateEtudiant(nxtSemestre);

            tasksMap.set(nxtKey, {
                id: nxtKey,
                text: nxtKey,
                start_date: dates.start,
                duration: item.nxt_duree_h ? Math.ceil(item.nxt_duree_h / 2) : DEFAULT_DURATION_DAYS,
                code_module: item.nxt_code_module, 
                duree_h: item.nxt_duree_h,
                type: item.nxt_type
            });
        }

        if (prvKey !== nxtKey){
            links.push({
                id: linkIdCounter++,
                source: prvKey,
                target: nxtKey,
                type: "0"
            });
        }
    });

    // Auto-scheduling 
    let hasChanged = true;
    let loopLimit = 100;

    while (hasChanged && loopLimit > 0) {
        hasChanged = false;
        loopLimit--;

        links.forEach(link => {
            const parent = tasksMap.get(link.source);
            const child = tasksMap.get(link.target);

            if (parent && child) {
                const parentStartDate = new Date(parent.start_date);
                const parentEndDate = new Date(parentStartDate);
                parentEndDate.setDate(parentEndDate.getDate() + parent.duration);

                const childStartDate = new Date(child.start_date);

                if (childStartDate < parentEndDate) {
                    child.start_date = formatDate(parentEndDate);
                    hasChanged = true;
                }
            }
        });
    }

    if (loopLimit === 0) {
        console.warn("Attention : Dépendance circulaire détectée dans les modules.");
    }

    return {
        data: Array.from(tasksMap.values()),
        links: links
    };
}


// ==========================================
// INITIALISATION ET CONFIGURATION DE DHTMLX
// ==========================================

function updateGanttChart(tasksData) {
    const ganttContainer = document.getElementById('gantt-chart');

    if (!tasksData || tasksData.data.length === 0) {
        ganttContainer.innerHTML = "<p style='color: gray; padding: 20px;'>Aucune donnée trouvée.</p>";
        return;
    }

    ganttContainer.innerHTML = "";
    gantt.config.date_format = "%Y-%m-%d";
    gantt.config.readonly = true;
    
    gantt.config.scale_unit = "month";
    gantt.config.date_scale = "%M %Y";
    gantt.config.min_column_width = 70;

    // Configuration de la grille à gauche
    gantt.config.columns = [
    {
        name: "text", 
        label: "Détails du module", 
        width: "200", 
        tree: true,
        template: function(task) {
            
            if (task.is_group) {
                return `<strong style="color:#2c3e50; font-size:1.1em;">📁 ${task.text}</strong>`;
            }
            const code = task.code_module || "N/A";
            const duree = task.duree_h ? `${task.duree_h}h` : "";
            const typeBadge = task.type ? `<span class="badge-type">${task.type}</span>` : "";

            // On retourne le HTML formaté
            return `
                <div style="display: flex; align-items: center; gap: 8px;">
                    <strong>${code}</strong> 
                    <span style="color: gray; font-size: 0.85em;">${duree}</span>
                    ${typeBadge}
                </div>
            `;
        }
    },
];

    gantt.init("gantt-chart");
    const observer = new ResizeObserver(() => gantt.setSizes());
    observer.observe(document.getElementById('gantt-chart'));
    gantt.clearAll();

    const treeData = [];
    const processedModules = new Set();

    // 1. On parcourt les tâches pour fabriquer l'arbre
    tasksData.data.forEach(task => {
        const moduleCode = task.code_module;

        if (moduleCode && !processedModules.has(moduleCode)) {
            treeData.push({
                id: `group_${moduleCode}`,       // ID unique pour le parent
                text: moduleCode,                // Le texte affiché
                is_group: true,                  // Marqueur perso pour le template HTML
                open: true,                      // Dossier ouvert par défaut
                type: gantt.config.types.project // Définit la tâche comme un projet global
            });
            processedModules.add(moduleCode);
        }

        // On indique à la tâche actuelle qui est son parent
        if (moduleCode) {
            task.parent = `group_${moduleCode}`;
        }
        
        // On ajoute la vraie tâche à la nouvelle liste
        treeData.push(task);
    });

    // On remplace les données plates par nos données hiérarchisées
    tasksData.data = treeData;


    gantt.parse(tasksData);

}


document.addEventListener("DOMContentLoaded", () => {
    const dropdowns = document.querySelectorAll('.select');
    const tagsContainer = document.getElementById('active-tags-container');
    const btnOpen = document.querySelector('.button-section button');
    const modal = document.getElementById('modal-ajout-module');
    const form = document.getElementById('form-ajout-module');
    const btnCancel_Cross = document.getElementById('btn-cancel-module-cross');
    const btnCancel = document.getElementById('btn-cancel-module');

    if (typeof dataGantt !== 'undefined') {
        const formattedData = transformDataForDHTMLX(dataGantt, userType);
        updateGanttChart(formattedData);
    } else {
        console.error("Les données dataGantt ne sont pas définies.");
    }

    if (btnOpen && modal) {
        btnOpen.addEventListener('click', (e) => {
            e.preventDefault();
            modal.showModal();
        });
    }

    if (btnCancel && modal || (btnCancel_Cross && modal)) {
        btnCancel.addEventListener('click', () => {
            modal.close();
            form.reset();
        });
        btnCancel_Cross.addEventListener('click', () => {
            modal.close();
            form.reset();
        });
    }

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault(); // Empêche le rechargement de la page

            const formData = new FormData(form);
            console.log("Données du formulaire :", Object.fromEntries(formData.entries()));

            const payload = {
                code_module: formData.get('code_module'),
                nom: formData.get('nom_module'),
                hCM: parseFloat(formData.get('hCM')) || 0,
                hTD: parseFloat(formData.get('hTD')) || 0,
                hTP: parseFloat(formData.get('hTP')) || 0,
                hProj: parseFloat(formData.get('hProjet')) || 0,
                hPerso: parseFloat(formData.get('hPerso')) || 0,
                ECTS: parseFloat(formData.get('ECTS')) || 0,
                semestre: parseInt(formData.get('semestre')),
                id_responsable: parseInt(formData.get('id_responsable')),
                id_discipline: parseInt(formData.get('id_discipline'))
            };
            console.log("Payload à envoyer :", payload);

            try {
                const response = await fetch(window.location.href, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(payload)
                    });

                if (response.ok) {
                    const result = await response.json();
                    alert("Module créé avec succès !");
                    modal.close();
                    form.reset();
                    window.location.reload();
                } else {
                    const error = await response.json();
                    alert("Erreur lors de la création : " + (error.detail || response.statusText));
                }

            } catch (err) {
                console.error("Erreur de requête :", err);
                alert("Impossible de joindre le serveur.");
            }
        });
    }

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('change', function() {
            const filterId = this.id;
            const selectedText = this.options[this.selectedIndex].text;
            const selectedValue = this.value;

            if (selectedValue === "") return;

            const isMultiple = (filterId === 'filiere-filter' || filterId === 'module-filter');

            if (isMultiple) {

                if (!activeFilters[filterId]) {
                    activeFilters[filterId] = new Set();
                }
                
                let alreadyExists = Array.from(activeFilters[filterId]).some(item => item.value === selectedValue);
                
                if (!alreadyExists) {
                    activeFilters[filterId].add({ value: selectedValue, text: selectedText });
                    createTag(filterId, selectedText, selectedValue);
                }
                
                this.selectedIndex = 0; 
                
            } else {
                activeFilters[filterId] = { value: selectedValue, text: selectedText };

                
                let existingTag = document.querySelector(`.filter-tag[data-filter="${filterId}"]`);

                if (existingTag) {
                
                    existingTag.querySelector('.tag-text').textContent = selectedText;
                    existingTag.setAttribute('data-value', selectedValue);
                } else {
                
                    createTag(filterId, selectedText, selectedValue);
                }
            }
        });
    });

    function createTag(filterId, text, value) {
        const tag = document.createElement('div');
            tag.classList.add('filter-tag');
            tag.setAttribute('data-filter', filterId);
            tag.setAttribute('data-value', value);

            tag.innerHTML = `
                <span class="tag-text">${text}</span>
                <button class="remove-tag" aria-label="Supprimer le filtre">&times;</button>
            `;

            tag.querySelector('.remove-tag').addEventListener('click', function() {
                tag.remove(); 

                const isMultiple = (filterId === 'filiere' || filterId === 'module');
                if (isMultiple) {
                    for (let item of activeFilters[filterId]) {
                        if (item.value === value) {
                            activeFilters[filterId].delete(item);
                            break;
                        }
                    }
                } else {
                    activeFilters[filterId] = null;
                    document.getElementById(filterId).value = ""; 
                }

            });

            tagsContainer.appendChild(tag);
    }
    const formattedData = transformDataForDHTMLX(dataGantt, userType);
    updateGanttChart(formattedData);
});