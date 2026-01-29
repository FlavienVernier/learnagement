// Composant des filières
// Affiche la liste des filières et gère l'ouverture de la modale
// Props: Aucune
// Composants importés:
// - ModaleFiliere: Composant de la modale
// - polytechLogo, usmbLogo: Images des logos
// - Loader: Composant d'indicateur de chargement

import {useEffect, useState} from "react";

import ModaleFiliere from "@/app/filieres/modaleFiliere";


/**
 * Composant des filières
 * Affiche la liste des filières et gère l'ouverture de la modale
 * 
 * @returns {JSX.Element} Composant React
 */
export default function ListFilieres({filieres} : {filieres: Filiere[]}){
    const [nomFiliereClicked, setNomFiliereClicked] = useState<string[]>([])
    const [imageExistsMap, setImageExistsMap] = useState<{ [key: string]: boolean }>({});
    const [imageExtensions, setImageExtensions] = useState<{ [key: string]: string }>({});
    const [attemptedExtensions, setAttemptedExtensions] = useState<{ [key: string]: boolean }>({});

    function filiereClicked(str: string){
        let filiere:Filiere|undefined = filieres.find((element: Filiere): boolean => str == element.nom_filiere)

        if(filiere != undefined){
            let nom_long:string = ""
            if(filiere.nom_long != undefined){
                nom_long = filiere.nom_long
            }
            setNomFiliereClicked([filiere.nom_filiere, nom_long])
        }
    }

    // Gestion des images
    const handleImage = (filiereName: string, status: string) => {
        if (status === 'load') {
            setImageExistsMap(prev => ({ ...prev, [filiereName]: true }));
        } else if (status === 'error') {
            // Si l'image n'existe pas avec l'extension actuelle, essayez avec l'autre extension
            const currentExtension = imageExtensions[filiereName] || 'svg';
            const newExtension = currentExtension === 'svg' ? 'png' : 'svg';

            // Vérifiez si nous avons déjà tenté de charger l'image avec l'autre extension
            if (!attemptedExtensions[filiereName]) {
                setImageExtensions(prev => ({ ...prev, [filiereName]: newExtension }));
                setAttemptedExtensions(prev => ({ ...prev, [filiereName]: true }));

                // Réessayez de charger l'image avec la nouvelle extension
                setImageExistsMap(prev => ({ ...prev, [filiereName]: false }));
            } else {
                // Si nous avons déjà tenté de charger l'image avec les deux extensions, marquez l'image comme non existante
                setImageExistsMap(prev => ({ ...prev, [filiereName]: false }));
            }
        }
    }


    return (
        <>
            <div className='w-full flex flex-wrap justify-center items-center gap-6'>
                {filieres.map((filiere) => {
                    const extension = imageExtensions[filiere.nom_filiere] || 'svg'

                    return (
                        <div
                            key={filiere.nom_filiere}
                            className=" relative
                                h-28 w-1/4 group cursor-pointer flex flex-col justify-center items-center
                                text-center shadow-md shadow-[rgba(193,193,193,0.45)] rounded-lg p-2 my-2
                                border border-[#e5e7eb] hover:bg-usmb-dark-blue hover:border-usmb-dark-blue
                            "

                            onClick={(): void => {
                                filiereClicked(filiere.nom_filiere);
                            }}
                        >
                            <img src={"/logos/" + filiere.nom_filiere.toLowerCase() + "." + extension}
                                 alt="Logo Polytech" width={24}

                                 onLoad={() => handleImage(filiere.nom_filiere, "load")}
                                 onError={() => handleImage(filiere.nom_filiere, "error")}

                                 className={`absolute top-2 left-2 ${!imageExistsMap[filiere.nom_filiere] && 'hidden'}`}
                            />

                            <p className="text-black text-2xl font-bold group-hover:text-white">
                                {filiere.nom_filiere}
                            </p>
                            <p className="text-gray-400 text-xs ">
                                {filiere.nom_long}
                            </p>
                        </div>
                    )
                })}
            </div>
            {nomFiliereClicked.length > 0 && (
                <ModaleFiliere
                    nomFiliere={nomFiliereClicked}
                    setNomFiliere={setNomFiliereClicked}
                />
            )}
        </>
        )
}