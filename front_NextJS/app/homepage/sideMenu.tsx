// Composant du menu latéral
// Affiche le menu de navigation de l'application
// Props: Aucune
// Composants importés:
// - LinkHomepage: Lien vers la homepage
// - ListModules: Liste des modules
// - Disconnection: Bouton de déconnexion
// - Loader: Composant d'indicateur de chargement

import Link from "next/link";
import ListModules from "@/app/modules/listModules";
import Disconnection from "@/app/connection/disconnection";

import HomeIcon from "@/public/homepage.svg";
import ListFiliereIcon from "@/public/list.svg"

/**
 * Composant du menu latéral
 * Affiche le menu de navigation de l'application
 * 
 * @returns {JSX.Element} Composant React
 */
export default function sideMenu(){
    return (
        <aside className={"col-span-1 h-screen p-2.5 flex flex-col justify-between items-center bg-usmb-dark-blue text-white"}>
            <ListModules />
            <div className={"w-full flex justify-center"}>
                <div className={"w-full flex flex-row justify-between items-center"}>
                    <Disconnection />
                    <Link href={'/homepage'}><HomeIcon width={28} height={28} className={"clickable-animation"} /></Link>
                    <Link href={'/'}><ListFiliereIcon width={38} height={38} className={"clickable-animation"} /></Link>
                </div>
            </div>
        </aside>
    )
}