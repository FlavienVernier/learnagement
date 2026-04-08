// Composant des composantes essentielles
// Affiche la liste des composantes essentielles d'une compétence
// Props:
// - composanteEssentielle: Tableau des composantes essentielles
// Composants importés:
// - Aucun

/**
 * Composant des composantes essentielles
 * Affiche la liste des composantes essentielles d'une compétence
 * 
 * @param {composanteEssentielle[]} composanteEssentielle - Tableau des composantes essentielles
 * @returns {JSX.Element} Composant React
 */
export default function ComposantesEssentielles({composantesEssentielles}:{composantesEssentielles: composanteEssentielle[]}){
    return (
        <div className={"w-2/4 px-1"}>
            <h4>Composantes essentielles</h4>
            <ul className={"list-disc list-inside"}>
                {composantesEssentielles.length > 0  ? composantesEssentielles.map((composante: composanteEssentielle) => (
                        <li key={composante.id_composante_essentielle}>{composante.libelle_composante_essentielle}</li>
                    )):
                    <p>Pas d'informations disponibles sur les composantes essentielles</p>
                }
            </ul>
        </div>

    )
}