// Composant de la homepage
// Affiche la page principale avec la charge de cours et les compétences
// Props: Aucune
// Composants importés:
// - ListCardsCharge: Composant pour afficher la charge de cours
// - ListFilieres: Composant pour afficher les filières
// - Loader: Composant d'indicateur de chargement

import axios from "axios";
import {useSession} from "next-auth/react";
import {useState, useEffect} from "react";
import {useRouter} from "next/navigation";

import ListCardsCharge from "@/app/homepage/charge/listCardsCharge";
import ListFilieres from "@/app/filieres/listFilieres"
import Loader from "@/app/indicators/loading";

/**
 * Composant de la homepage
 * Affiche la page principale avec la charge de cours et les compétences
 * 
 * @returns {JSX.Element} Composant React
 */
export default function Homepage(){
    const {data: session, status} = useSession()
    const router = useRouter()

    const [filieres, setNomFilieres] = useState<Filiere[]>([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        if(status == 'unauthenticated'){
            router.push('/connection')
        }
    }, [session, router]);

    useEffect(() => {

        axios.get('/api/proxy/list/listUserFilieres', {withCredentials: true})
            .then(response => {
                if (response.status == 200){
                    setNomFilieres(response.data)
                    setIsLoading(false)
                }else{
                    console.log('error : filiere.tsx')
                }
            })

    }, []);

    return(
        <>
            {session && <h1>Bonjour, {session.user.firstname} ! 👋</h1>}
            <div className={"h-screen flex flex-col items-center justify-around"}>
                <div className={"w-full self-start"}>
                    <h3>Ma charge de cours</h3>
                    <ListCardsCharge />
                </div>
                <div className={"w-full self-start"}>
                    <h3>Compétences par filières</h3>
                    {isLoading ? <Loader /> : <ListFilieres filieres={filieres} />}
                </div>
            </div>
        </>
    )
}