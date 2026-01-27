"use client";

export default function AlertBox({text, color}: { text:string, color:string }){

    return(
        <div className={"absolute top-5 left-1/2 transform -translate-x-1/2 w-48 h-12 px-5 rounded-lg flex items-center shadow-md text-white" + " " + color}>
            <p>{text}</p>
        </div>
    )
}