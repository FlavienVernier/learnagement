import { create } from 'zustand'
import { persist } from 'zustand/middleware'

type ListModules = {
    listModules: Record<number, ModuleInfos>,
    charged: boolean,
    setListModules: (module: Record<number, ModuleInfos>) => void,
    setCharged: (charged: boolean) => void
    reset: () => void
}
export const useListModulesStore = create<ListModules>() (
    persist(
        (set) => ({
            listModules: {},
            charged: false,
            setListModules: (modules) => set({ listModules: modules }),
            setCharged: (charged) => set({ charged }),
            reset: () => set({ listModules: {}, charged: false })
        }),
        {
            name: 'list-modules-storage', // nom de la clé dans localStorage
        }
    )
)

