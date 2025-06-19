// Composant de la liste des modules
// Affiche la liste des modules avec leur statut (avec ou sans APC)
// Props: Aucune
// Composants importés:
// - useListModulesStore: Store pour la gestion des modules
// - useSession: Hook d'authentification
// - useSearchParams: Hook pour accéder aux paramètres de recherche

"use client"

import {useEffect, useState} from "react";
import {useListModulesStore} from "@/app/store/useListModulesStore";
import {useSession} from "next-auth/react";
import {useSearchParams} from "next/navigation";

import Link from "next/link";
import axios from "axios";

/**
 * Composant de la liste des modules
 * Affiche la liste des modules avec leur statut (avec ou sans APC)
 * 
 * @returns {JSX.Element} Composant React
 */
export default function ListModule(){
    const {listModules} = useListModulesStore()
    const [moduleClicked, setModuleClicked] = useState(-1)
    const [idModulesHasApc, setIdModulesHasApc] = useState<string[]>([])

    const searchParams = useSearchParams()
    const  id_module = searchParams.get("id_module")

    useEffect(() => {
        if (id_module != undefined){
            setModuleClicked(parseInt(id_module))
        }
    }, [searchParams]);

    useEffect(() => {
        let form_data = new FormData
        form_data.append("indexBy", "id_module")
        axios.post("/api/proxy/list/listModulesOfAllAPC", form_data, {withCredentials: true})
            .then(response => {
                let data = response.data
                setIdModulesHasApc(Object.keys(data))
            })
    }, []);

    const modulesAvecAPC = Object.values(listModules).filter((m: ModuleInfos) => idModulesHasApc.includes(m.id_module.toString()));
    const modulesSansAPC = Object.values(listModules).filter((m: ModuleInfos) => !idModulesHasApc.includes(m.id_module.toString()));

    function renderModule(module: ModuleInfos, hasAPC: boolean) {
        return (
            <Link  key={module.id_module} href={{pathname : '/modules', query: {id_module: module.id_module}}} className={"flex justify-center items-center"}>
                <div
                    id={String(module.id_module)}
                    className={`clickable-animation w-[95%] h-20 mb-2.5 pl-2.5 rounded-lg cursor-pointer ${
                        hasAPC ?
                            `hover:bg-usmb-blue ${ moduleClicked === module.id_module ? "bg-usmb-blue" : "bg-usmb-cyan" }`
                        : `border border-red-500 text-gray-300 hover:bg-red-500/80 ${moduleClicked === module.id_module ? "bg-red-500/80" : "bg-red-500/60"   }` 
                        }`
                    }
                >
                    <p className={"font-medium"}>{module.nom}</p>
                    <p>{module.code_module}</p>
                </div>
            </Link>
        );
    }

    return (
        <div className={"h-3/4 flex flex-col overflow-y-auto"}>
            {modulesAvecAPC.length > 0 && modulesSansAPC.length > 0 ? (
                <>
                    <h4>Modules (avec APC)</h4>
                    {modulesAvecAPC.map((module: ModuleInfos) => renderModule(module, true))}
                    <div className={"border-t border-gray-400 my-4"} />
                    <h4>Modules (sans APC)</h4>
                    {modulesSansAPC.map((module: ModuleInfos) => renderModule(module, false))}
                </>

            ) : modulesSansAPC.length > 0 && modulesAvecAPC.length == 0 ? (
                <>
                    <p>Aucun modules avec APC</p>
                    <div className={"border-t border-gray-400 my-4"} />
                    <h4 className={'text-lg'}>Modules (sans APC)</h4>
                    {modulesSansAPC.map((module: ModuleInfos) => renderModule(module, false))}
                </>
            ):(
                <>
                    <h4 className={'text-lg'}>Modules (avec APC)</h4>
                    {modulesAvecAPC.map((module: ModuleInfos) => renderModule(module, true))}
                    <div className={"border-t border-gray-400 my-4"} />
                    <p>Aucun modules sans APC</p>
                </>
            )}

        </div>
    );
}