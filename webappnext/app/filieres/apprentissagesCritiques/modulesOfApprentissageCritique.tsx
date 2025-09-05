// Composant des modules d'apprentissage critique
// Affiche la liste des modules associés à un apprentissage critique
// Props:
// - listModules: Tableau des modules
// Composants importés:

import Link from "next/link";
import {useSession} from "next-auth/react";

/**
 * Composant des modules d'apprentissage critique
 * Affiche la liste des modules associés à un apprentissage critique
 * 
 * @param {ModuleOfApc[]} listModules - Tableau des modules
 * @returns {JSX.Element} Composant React
 */
export default function ModulesOfApprentissageCritique({listModules}:{listModules:ModuleOfApc[]}){
    const {data: session} = useSession()

    return(
        <div className={`shadow-md rounded-b-lg bg-white`}>
            <p className={`border-t border-gray-300`}></p>
            <div className="p-2">
                <ul className={`list-disc list-inside text-sm/6`}>
                    {listModules.map((module: ModuleOfApc) => {
                        if (session && module.id_responsable == parseInt(session.user.id)){
                            return(
                                <Link key={module.id_module}
                                      href={{pathname: '/modules', query: {id_module: module.id_module}}}>
                                    <li className="cursor-pointer">
                                        <span className={"underline text-usmb-blue hover:text-usmb-dark-blue"}>
                                            {module.code_module} - {module.nom}
                                        </span>
                                    </li>
                                </Link>
                            )
                        }else{
                            return (
                                <li key={module.id_module}>{module.code_module} - {module.nom}</li>
                            )
                        }

                    })}
                </ul>
            </div>

        </div>
    )
}