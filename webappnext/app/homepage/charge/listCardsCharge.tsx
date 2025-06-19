import axios from "axios";
import {useEffect, useState} from "react";
import { ChargeState, ChargeType } from "@/app/types/charge/charges";
import {useSession} from "next-auth/react";
import CardCharge from "@/app/homepage/charge/cardCharge";
import Loader from "@/app/indicators/loading";
import SetCookie from "@/app/connection/setCookie";
import {User} from "next-auth";

export default function ListCardsCharge(){
    const {data: session} = useSession()
    const [charges, setCharges] = useState<ChargeState>({
        Charge: -1,
        CM: -1,
        TD: -1,
        TP: -1
    })
    const [isLoading, setIsLoading] = useState(true)

    const chargeTypes: ChargeType[] = ['CM', 'TD', 'TP'];
    const chargeTotCmTdTp = charges.CM + charges.TD + charges.TP

    useEffect(() => {
        if (session){
            let form_data = new FormData()
            form_data.append("user_id", session.user.id)
            axios.post("/api/proxy/select/selectChargeEnseignant", form_data,{withCredentials: true})
                .then(response => {
                    if (response.status == 200){
                        setCharges(response.data)
                        setIsLoading(false)
                    }else{
                        console.log('erreur')
                    }
                })
        }

    }, [session]);


        if (isLoading){
            return <Loader />
        }else{
            return(
                <div className={"w-full flex flex-grow justify-evenly"}>
                    {charges.Charge == chargeTotCmTdTp ? 
                        <CardCharge label={'TOTAL'} dataDonut={[charges.CM, charges.TD, charges.TP]}/>
                        :
                        <CardCharge label={'TOTAL'} dataDonut={[charges.CM, charges.TD, charges.TP, charges.Charge - chargeTotCmTdTp]}/>
                    }
                    {chargeTypes.map((type) => (
                        <CardCharge
                            key={type}
                            label={type}
                            dataDonut={[charges[type], charges.Charge - charges[type]]}
                        />
                    ))}
                </div>
            )
        }
}