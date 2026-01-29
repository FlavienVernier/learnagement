import {useEffect, useState} from "react";

import Donut from "@/app/homepage/charge/donutCharge";

export default function CardCharge({label, dataDonut}:{label:string, dataDonut: number[]}){
    return(

        <div className={"h-56 w-56 shadow-md rounded-lg flex flex-col items-center justify-between py-2"}>
            <h3 className={"text-2xl font-bold mb-0 ml-0"}>{label}</h3>
            <Donut label={label} dataDonut={dataDonut}/>
        </div>

    )
}