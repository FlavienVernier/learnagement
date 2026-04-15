const activeFilters = {};
let myGantt = null;

console.log("token", token);

console.log("id utilisateur", userId);

// console.log("Données des modules :", dataModules);
// console.table(dataModules);

// console.log("Données des promos :", dataPromos);
// console.table(dataPromos);

// console.log("Données des filières :", dataFilieres);
// console.table(dataFilieres);

console.log("Données des dépendances de modules :", dataModulesDependencies);
console.table(dataModulesDependencies);

 console.log("Données des reponsables modules :", dataModulesResponsables);

 console.log("Données des intervenant par id :");
    console.table(dataModulesIntervenantById);

let tasks_test = [
  {
    "id": "T1",
    "name": "Mathématiques - Semestre 1",
    "start": "2023-09-01",
    "end": "2023-12-20",
    "progress": 100,
    "dependencies": ""
  },
  {
    "id": "T2",
    "name": "Physique Appliquée",
    "start": "2024-01-05",
    "end": "2024-04-15",
    "progress": 30,
    "dependencies": "T1" 
  }
]

function updateGanttChart(tasks) {
    const svgContainer = document.getElementById('gantt-chart');

    if (!tasks || tasks.length === 0) {
        svgContainer.innerHTML = "<text x='20' y='30' fill='gray'>Aucune donnée trouvée pour ces filtres.</text>";
        myGantt = null;
        return;
    }

    if (myGantt) {
        myGantt.refresh(tasks);
    } 
    else {
        myGantt = new Gantt("#gantt-chart", tasks, {
            header_height: 50,
            column_width: 30,
            step: 24,
            view_modes: ['Quarter Day', 'Half Day', 'Day', 'Week', 'Month'],
            bar_height: 25,
            bar_corner_radius: 4,
            arrow_curve: 5,
            padding: 18,
            view_mode: 'Week',
            date_format: 'YYYY-MM-DD',
            language: 'fr',
            
            
            on_click: function (task) {
                console.log("Tu as cliqué sur le module :", task.name);
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const dropdowns = document.querySelectorAll('.select');
    const tagsContainer = document.getElementById('active-tags-container');
    const btnOpen = document.querySelector('.button-section button');
    const modal = document.getElementById('modal-ajout-module');
    const form = document.getElementById('form-ajout-module');
    const btnCancel = document.getElementById('btn-cancel-module');

    if (btnOpen && modal) {
        btnOpen.addEventListener('click', (e) => {
            e.preventDefault();
            modal.showModal();
        });
    }

    // 2. Fermer la modale
    if (btnCancel && modal) {
        btnCancel.addEventListener('click', () => {
            modal.close();
            form.reset(); // Réinitialise les champs si on annule
        });
    }

    // 3. Gérer la soumission du formulaire
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault(); // Empêche le rechargement de la page

            // Récupération des données du formulaire
            const formData = new FormData(form);

            // Construction du JSON selon tes besoins backend
            const payload = {
                code_module: formData.get('code_module'),
                nom: formData.get('nom'),
                hCM: parseFloat(formData.get('hCM')) || 0,
                hTD: parseFloat(formData.get('hTD')) || 0,
                hTP: parseFloat(formData.get('hTP')) || 0,
                semestre: parseInt(formData.get('semestre')),
                id_responsable: parseInt(formData.get('id_responsable')),
                promos: formData.getAll('promos[]').map(Number),
                dependances_avant: formData.getAll('dependances_avant[]').map(Number),
                dependances_apres: formData.getAll('dependances_apres[]').map(Number)
            };

            // Récupération du token (assure-toi que cette variable est définie dans ton PHP/JS)
            // ex en PHP: echo "<script>const userToken = '$token';</script>";
            const token = typeof userToken !== 'undefined' ? userToken : '';

            try {
                // Envoi à l'API Python (modifie l'URL selon ton routage)
                const response = await fetch('/api/modules/', {
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
                    window.location.reload(); // Rafraîchit pour voir le nouveau module
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

                // On cherche s'il y a déjà un tag pour cette catégorie (ex: Période)
                let existingTag = document.querySelector(`.filter-tag[data-filter="${filterId}"]`);

                if (existingTag) {
                    // On le met à jour s'il existe
                    existingTag.querySelector('.tag-text').textContent = selectedText;
                    existingTag.setAttribute('data-value', selectedValue);
                } else {
                    // Sinon on le crée
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
    updateGanttChart(tasks_test);
});