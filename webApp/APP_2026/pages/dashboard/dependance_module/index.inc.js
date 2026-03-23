document.addEventListener("DOMContentLoaded", () => {
    const dropdowns = document.querySelectorAll('.filter-dropdown');
    const tagsContainer = document.getElementById('active-tags-container');

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('change', function() {
            const filterId = this.id;
            const selectedText = this.options[this.selectedIndex].text;
            const selectedValue = this.value;

            if (selectedValue === "") {
                removeTagFromDOM(filterId);
                return;
            }

            let existingTag = document.querySelector(`.filter-tag[data-filter="${filterId}"]`);

            if (existingTag) {
                existingTag.querySelector('.tag-text').textContent = selectedText;
            } else {
                // Crée un nouveau tag
                createTag(filterId, selectedText);
            }
        });
    });

    // Fonction pour créer la balise HTML du tag
    function createTag(filterId, text) {
        const tag = document.createElement('div');
        tag.classList.add('filter-tag');
        tag.setAttribute('data-filter', filterId);

        tag.innerHTML = `
            <span class="tag-text">${text}</span>
            <button class="remove-tag" aria-label="Supprimer le filtre">&times;</button>
        `;

        // Événement pour la petite croix (supprimer)
        tag.querySelector('.remove-tag').addEventListener('click', function() {
            removeTagFromDOM(filterId);
            // Remet le select correspondant sur la valeur par défaut
            document.getElementById(filterId).value = "";
        });

        tagsContainer.appendChild(tag);
    }

    // Fonction pour supprimer le tag de l'affichage
    function removeTagFromDOM(filterId) {
        const tag = document.querySelector(`.filter-tag[data-filter="${filterId}"]`);
        if (tag) {
            tag.remove();
        }
    }
});