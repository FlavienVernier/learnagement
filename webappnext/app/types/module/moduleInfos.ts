type ModuleInfos = {
    id_module: number,
    code_module: string,
    nom: string,
    ECTS?: number,
    id_discipline: number,
    id_semestre: number,
    hCM?: number,
    hTD?: number,
    hTP?: number,
    hTPTD?: number,
    hproj?: number,
    hPersonnelle?: number,
    id_responsable?: number,
    id_etat_module?: number,
    commentaire?: string,
    modifiable?: number,
    has_learning_unit: boolean
}