"use client"

import {useEffect, useState} from "react";
import {useInfosModuleStore} from "@/app/store/useInfosModuleStore";
import {useListModulesStore} from "@/app/store/useListModulesStore";
import {useSearchParams} from "next/navigation";

import SideMenu from "@/app/homepage/sideMenu"
import Maquette from './maquetteModule/maquetteModule'
import Link from "next/link";
import axios from "axios";

interface apcOfModule{
    id_apprentissage_critique: number,
    libelle_apprentissage: string
}
export default function Page(){
    const {module, setModule} = useInfosModuleStore()
    const {listModules} = useListModulesStore()
    const [listApc, setListApc] = useState<apcOfModule[]>([])
    const searchParams = useSearchParams()
    const id_module = searchParams.get("id_module")

    useEffect(() => {
        if (id_module){
            setModule(listModules[parseInt(id_module)])
        }
    }, [id_module, listModules]);

    useEffect(() => {
        if (id_module){
            let form_data = new FormData()
            form_data.append("id_module", id_module)
            axios.post('/api/proxy/list/listAPCbyIdModule',form_data,{withCredentials: true})
                .then(response => {
                    setListApc(response.data)
                })
        }

    }, [id_module]);

    return (
        <main className={"h-screen grid grid-cols-4"}>
            <SideMenu />
            <div className={"col-span-3 overflow-y-auto"}>
                <div className={"h-screen flex flex-col items-center"}>
                    {module != undefined ? (
                        <>
                            <div>
                                <h1 className={"font-bold text-4xl mb-5"}>
                                    {(module.code_module != null && module.nom != null) && <>{module.code_module} - {module.nom}</>}
                                </h1>
                                <div className={"w-full flex justify-around font-bold"}>
                                    {module.hCM != null && <p>Heures CM : {module.hCM}</p>}
                                    {module.hTD != null && <p>Heures TD : {module.hTD}</p>}
                                    {module.hTP != null && <p>Heures TP : {module.hTP}</p>}
                                </div>

                                <ul className={"m-2 mt-4 list-disc list-inside"}>
                                    {listApc.length > 0 && (
                                        listApc.map((apc: apcOfModule) => (
                                            <li key={apc.id_apprentissage_critique}>{apc.libelle_apprentissage}</li>
                                        ))
                                    )}
                                </ul>
                            </div>
                            {module.nom != null && <Maquette code_module={module.code_module}/>}
                        </>
                        ):(
                            <div className={"w-fulll h-screen flex flex-col justify-center items-center gap-3"}>
                                <p>Il semblerait qu'il y est une erreur !</p>
                                <Link href={'/homepage'} className={"button"}>Retourner à l'acceuil</Link>
                            </div>
                    )
                    }
                </div>
            </div>
        </main>

    )
}