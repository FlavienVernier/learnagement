// Composant de la modale des filières
// Affiche les détails d'une filière sélectionnée
// Props:
// - nomFiliere: Tableau contenant le nom de la filière
// - setNomFiliere: Fonction pour mettre à jour le nom de la filière
// Composants importés:
// - ListCompetences: Liste des compétences
// - ComposantesEssentielles: Liste des composantes essentielles
// - ListApprentissagesCritiques: Liste des apprentissages critiques
// - cross: Image de la croix pour fermer la modale

import {useEffect, useState} from "react";
import Image from "next/image";
import axios from "axios";

import ListCompetences from "@/app/filieres/listCompetences"
import ComposantesEssentielles from "@/app/filieres/composantesEssentielles"
import ListApprentissagesCritiques from "@/app/filieres/apprentissagesCritiques/listApprentissagesCritiques"

import cross from "@/public/white-cross.png"

/**
 * Composant de la modale des filières
 * Affiche les détails d'une filière sélectionnée
 * 
 * @param {string[]} nomFiliere - Nom de la filière sélectionnée
 * @param {Function} setNomFiliere - Fonction pour mettre à jour le nom de la filière
 * @returns {JSX.Element} Composant React
 */
export default function ModaleFiliere({nomFiliere, setNomFiliere}: { nomFiliere: string[], setNomFiliere: any }) {
    const [infosCompetences, setInfosCompetences] = useState<infosCompetence[]>([])
    const [idCompetenceClicked, setIdCompetenceClicked] = useState<number>(-1)
    const [composantesEssentielles, setComposantesEssentielles] = useState<composanteEssentielle[]>([])

    useEffect(() => {
        // Désactivation du scroll de la page en fond de la modale quand la modale s'ouvre.
        document.body.style.overflow = 'hidden';
        return () => {
            document.body.style.overflow = 'auto';
        };
    }, []);

    useEffect(() => {
        let form_data = new FormData
        form_data.append("nom_filiere", nomFiliere[0])
        axios.post("/api/proxy/list/listCompetencesOfFiliere", form_data, {withCredentials: true})
            .then(response => {
                setInfosCompetences(response.data)
            })
        setIdCompetenceClicked(-1)
    }, [nomFiliere]);

    useEffect(() => {
        if(idCompetenceClicked >= 0){
            let form_data = new FormData
            form_data.append("idCompetence", idCompetenceClicked.toString())
            axios.post("/api/proxy/list/listComposanteEssentielle", form_data, {withCredentials: true})
                .then(response => {
                    setComposantesEssentielles(response.data)
                })
        }else{
            setComposantesEssentielles([]);
        }

    }, [idCompetenceClicked]);

    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if(event.key == "Escape"){
                closeModale()
            }
        };

        window.addEventListener("keydown", handleKeyDown);

        return (): void => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    }, []);

    function closeModale(){
        setNomFiliere([]);
        setIdCompetenceClicked(-1)
    }

    return(
        <div className={"foreground-full flex justify-center items-center"} onClick={closeModale}>
            <div className={"w-[90%] h-4/5 p-4 rounded-lg bg-white overflow-auto"} onClick={(e) => {
                e.stopPropagation()
            }}>
                <div className={"relative"}>
                    <span onClick={closeModale} className={"absolute top-0 right-0 p-3 rounded-full bg-usmb-red hover:bg-red-600 cursor-pointer"}><Image src={cross} alt={'white cross'} width={24} height={24} /></span>
                    <h1 className={"mt-0 mb-8"}>{nomFiliere[1] != null ? <>{nomFiliere[0]} - {nomFiliere[1]}</>  : nomFiliere[0]}</h1>
                    <ListCompetences infosCompetences={infosCompetences} setIdCompetenceClicked={setIdCompetenceClicked} />
                    <div className={"w-full flex flex-row justify-between"}>
                        <ComposantesEssentielles composantesEssentielles={composantesEssentielles}/>
                        {idCompetenceClicked >= 0 && <ListApprentissagesCritiques idCompetence={idCompetenceClicked}/>}
                    </div>
                </div>
            </div>
        </div>
    )
}