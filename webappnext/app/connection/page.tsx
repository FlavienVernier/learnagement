// Composant de connexion
// Gère l'authentification des utilisateurs
// Props: Aucune

"use client"

import React, {useEffect, useState} from "react";
import {useRouter, useSearchParams} from "next/navigation"
import Image from "next/image";
import {signIn, useSession} from "next-auth/react"
import Link from "next/link";
import {z} from "zod"

import leftArrow from "@/public/left-arrow.png"



/**
 * Composant de connexion
 * Gère la page de connexion avec formulaire et gestion des erreurs
 * 
 * @returns {JSX.Element} Composant React
 */
export default function Page() {
    const {data: session, status} = useSession()
    const router = useRouter();
    const searchParams = useSearchParams();

    const [login, setLogin] = useState('')
    const [mdp, setMdp] = useState('')
    const [loggError, setLoggingError] = useState(false)
    const [msgLoggErr, setMsgLoggErr] = useState<string | undefined>('')
    const [loginMsgError, setLoginMsgError] = useState<string | undefined>(undefined)
    const [mdpMsgError, setMdpMsgError] = useState<string | undefined>(undefined)

    const schema = z.object({
        email: z.string().email(),
        password: z.string().min(4, "Password must contain at least 4 character(s)"),
    });

    // fonctions qui permettent d'afficher les messages d'erreurs en cas de mauvais remplissage des input
    // (handleValidation, handleLogin, handleMdp)
    function handleValidation(formData: object, schema: z.Schema, fieldName: string, setErrorMsg: any) {
        const result = schema.safeParse(formData)
        if (!result.success) {
            const formatted = result.error.format() as unknown as { [key: string]: { _errors: string[] } }
            console.log(formatted)

            setErrorMsg(formatted[fieldName]?._errors[0])
        }else{
            setErrorMsg(undefined)
        }
    }

    function handleLogin() {
        let formData = {
            email: login,
        };
        handleValidation(formData, schema, 'email', setLoginMsgError);
    }

    function handleMdp() {
        let formData = {
            password: mdp
        };
        handleValidation(formData, schema, 'password', setMdpMsgError);
    }

    useEffect(() => {
        if (status == 'authenticated'){
            router.push('/homepage')
        }

        // Vérifier si l'URL contient un paramètre d'erreur
        const error = searchParams.get('error')
        if (error === 'CredentialsSignin') {
            setLoggingError(true)
            setMsgLoggErr('Identifiant ou mot de passe incorrect')
        }
    }, [session, router, searchParams]);


    const credentialsAction = (formData: FormData) => {
        let credentials = Object.fromEntries(formData.entries())
        let formDataForZod = {
            email: credentials.username,
            password: credentials.password
        }

        if(schema.safeParse(formDataForZod).success){
            signIn("credentials", credentials)
        }
    }

    return (
        <div className={"w-screen h-screen flex justify-center items-center"}>
            <form className={"flex flex-col items-center justify-center pt-4 p-3 shadow-lg"} action={credentialsAction}>
                <Link href={"/"} className={"self-start"}><Image src={leftArrow} alt="left arrow" width={24} height={24} /></Link>
                <div className={"flex flex-col px-9 pb-9 pt-5"}>
                    <div className={"mb-2"}>
                        <label htmlFor="credentials-username">Login :</label>
                        <input type="mail" id="credentials-username" name="username" required={true} value={login}
                               onChange={e => setLogin(e.target.value)} onBlur={handleLogin}/>
                        {loginMsgError != undefined && <p className={"text-usmb-red self-center text-xs"}>{loginMsgError}</p>}
                    </div>

                    <div className={"mb-7"}>
                        <label htmlFor="credentials-password">Mot de passe :</label>
                        <input type="password" id="credentials-password" name="password" required={true} value={mdp}
                               onChange={e => setMdp(e.target.value)} onBlur={handleMdp}/>
                        {mdpMsgError != undefined && <p className={"text-usmb-red self-center text-xs"}>{mdpMsgError}</p>}
                    </div>
                    {loggError && <p className={"text-usmb-red self-center mb-7"}>{msgLoggErr}</p>}
                    <button type="submit" className={"self-center bg-usmb-cyan"}>Se connecter</button>
                </div>
                <Link href={'/activateAccount'} className={"text-xs underline text-usmb-cyan cursor-pointer"}>Activer mon compte</Link>
            </form>
        </div>

    )
}
