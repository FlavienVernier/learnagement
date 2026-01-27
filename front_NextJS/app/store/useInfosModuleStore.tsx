import { create } from 'zustand'

export const useInfosModuleStore = create<Module>()((set) => ({
    module: {
        id_module: -1,
        code_module: "",
        nom: "",
        ECTS: -1,
        id_discipline: -1,
        id_semestre: -1,
        hCM: -1,
        hTD: -1,
        hTP: -1,
        hTPTD: -1,
        hproj: -1,
        hPersonnelle: -1,
        id_responsable: -1,
        id_etat_module: -1,
        commentaire: "",
        modifiable: -1},
    setModule: (moduleInfos: ModuleInfos) => set({module: moduleInfos}), /* Mise à jour des infos du module */
    // setLoggedin: (bool: boolean) => set((state) => ({user: {...state.user, loggedin:bool}}))
}))