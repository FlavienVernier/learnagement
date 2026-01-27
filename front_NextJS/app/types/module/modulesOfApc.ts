interface ModuleOfApc {
    id_apprentissage_critique: number,
    id_module: number,
    code_module: string,
    nom: string,
    id_responsable: number
}

interface ModulesOfAPC{
    [key: number]: ModuleOfApc[]
}
