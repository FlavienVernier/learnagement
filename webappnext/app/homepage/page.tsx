"use client"

import axios from "axios";
import {useSession} from "next-auth/react";
import {useListModulesStore} from "@/app/store/useListModulesStore";
import SideMenu from "@/app/homepage/sideMenu"
import Homepage from "@/app/homepage/homepage";
import {Suspense, useEffect} from "react";
import Loader from "@/app/indicators/loading";

export default function Home() {
    const {data: session} = useSession()
    const {charged, setListModules, setCharged} = useListModulesStore()

    useEffect(() => {
        if (session && !charged){
            let form_data = new FormData
            form_data.append("userId", session.user.id)
            axios.post("/api/proxy/list/listResponsableModule", form_data, {withCredentials: true})
                .then(response => {
                    setListModules(response.data)
                    setCharged(true) // Permet de charger une seule fois ListModules, quand l'utilisateur se connecte pour la première fois
                })
        }
    }, [session]);

    return (
        <>
            <main className={"h-screen grid grid-cols-4"}>
                <SideMenu />
                <div className={"col-span-3 overflow-y-auto"}>
                    <Homepage />
                </div>
          </main>
      </>
    );
}