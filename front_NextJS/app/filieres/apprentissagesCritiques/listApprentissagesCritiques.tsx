// Composant de la liste des apprentissages critiques
// Affiche la liste des apprentissages critiques d'une compétence
// Props:
// - idCompetence: Identifiant de la compétence
// Composants importés:
// - plus, moins: Images pour les boutons d'expansion
// - ModulesOfApprentissageCritique: Liste des modules associés aux apprentissages critiques

import axios from "axios";

import { useEffect, useState} from "react";
import {isEmpty} from "@jsonjoy.com/util/lib/isEmpty";
import plus from "@/public/plus.png"
import moins from "@/public/signe-moins-dune-ligne-en-position-horizontale.png"

import ModulesOfApprentissageCritique from "@/app/filieres/apprentissagesCritiques/modulesOfApprentissageCritique"
import Image from "next/image";


/**
 * Composant de la liste des apprentissages critiques
 * Affiche la liste des apprentissages critiques d'une compétence
 * 
 * @param {number} idCompetence - Identifiant de la compétence
 * @returns {JSX.Element} Composant React
 */
export default function ListApprentissagesCritiques({idCompetence}:{idCompetence: number}) {
    const [apprentissagesCritiques, setApprentissagesCritiques] = useState<apprentissagesCritiquesStruct>({})
    const [apcAsModule, setApcAsModule] = useState<ModulesOfAPC>({})

    const [levels, setLevels] = useState<string[]>([])
    const [levelClicked, setLevelClicked] = useState<number>(-1)

    const [idApcClicked, setApcClicked] = useState<number>(-1)


    useEffect(() => {
        if (levels.length > 0 && apprentissagesCritiques != undefined){
            let default_level: string = levels[0]
            setLevelClicked(parseInt(default_level))
        }
    }, [levels, apprentissagesCritiques]);

    useEffect(() => {
        let form_data = new FormData
        form_data.append("idCompetence", idCompetence.toString())
        axios.post("/api/proxy/list/listApprentissagesCritiques", form_data, {withCredentials: true})
            .then(response => {
                let data = response.data
                setApprentissagesCritiques(data)
                setLevels(Object.keys(data))
            })
    }, [idCompetence]);

    useEffect(() => {
        let form_data = new FormData
        form_data.append("indexBy", "id_apprentissage_critique")
        axios.post("/api/proxy/list/listModulesOfAllAPC", form_data, {withCredentials: true})
            .then(response => {
                setApcAsModule(response.data)
            })
    }, []);

    function levelOfApcToShow(event: any) {
        let text_event: string = event.target.innerText
        let level: string[] = text_event.split(" ")
        setLevelClicked(parseInt(level[1]))
    }

    function showModules(idApc: number){

        if (idApcClicked == idApc){
            setApcClicked(-1)
        }else if(idApc in Object.keys(apcAsModule)){
            setApcClicked(idApc)
        }
    }

    return(
        <div className={"w-2/4 px-1 flex flex-col gap-4"}>
            {/* Affichage des niveaux */}
            <div className={"flex flex-row justify-around"}>
                {levels.map((level: string) => (
                    <div id={level} key={level} className={`w-32 h-14 px-2 flex justify-center items-center rounded-lg text-white cursor-pointer
                            ${levelClicked.toString() === level ? 'bg-usmb-blue' : 'bg-usmb-cyan'}`}

                         onClick={levelOfApcToShow}
                    >
                        <p className={"font-semibold text-base/5"}>niveau {level}</p>
                    </div>
                ))}
            </div>

            <div className={"flex flex-col gap-4"}>
                {/* Affichage des APC*/}
                {(!isEmpty(apprentissagesCritiques) && levelClicked >= 0 && Object.keys(apcAsModule).length > 0) && (
                    apprentissagesCritiques[levelClicked].map((apc: apprentissageCritique) => (
                        <div key={apc.id_apprentissage_critique}>
                            <div id={apc.id_apprentissage_critique.toString()}
                                 className={`flex justify-between items-center p-2 shadow-md font-medium bg-white
                                 ${(apc.id_apprentissage_critique in Object.keys(apcAsModule)) ? 
                                     'cursor-pointer' : 'cursor-not-allowed'
                                 }
                                 ${idApcClicked === apc.id_apprentissage_critique ? 'rounded-t-lg' : 'rounded-lg'}
                                 `}

                                 onClick={() => {showModules(apc.id_apprentissage_critique)}}
                            >
                                <p className={"max-w-[90%]"}>{apc.libelle_apprentissage}</p>
                                {(apc.id_apprentissage_critique in Object.keys(apcAsModule)) && (
                                    <>
                                        {idApcClicked > -1 && idApcClicked === apc.id_apprentissage_critique ? (
                                            <Image src={moins} alt={"icon moins"} width={24} className={"w-6 h-6"} />
                                        ) : (
                                            <Image src={plus} alt={"icon plus"} width={24} className={"w-6 h-6"} />
                                        )}
                                    </>
                                )}

                            </div>
                            {
                                idApcClicked > -1 && idApcClicked === apc.id_apprentissage_critique && (
                                    <ModulesOfApprentissageCritique listModules={apcAsModule[idApcClicked]} />
                                )
                            }
                        </div>
                    ))
                )}
            </div>
        </div>
    )
}