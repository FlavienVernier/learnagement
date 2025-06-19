'use client'

import axios from "axios";
import {signOut} from "next-auth/react";
import {useListModulesStore} from "@/app/store/useListModulesStore";
import {useRouter} from "next/navigation";
import LogoutIcon from "@/public/logout.svg"

export default function Disconnection(){
    const resetStore = useListModulesStore.getState().reset
    const router = useRouter()

    function sendDeconnection() {
        axios.get("/api/proxy/connection/logout", { withCredentials: true })
        resetStore()
        signOut()
    }

    return(
        <LogoutIcon width={35} height={35} onClick={sendDeconnection} className={"clickable-animation cursor-pointer"}/>
    )
}