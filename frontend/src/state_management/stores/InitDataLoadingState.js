import { create } from 'zustand';


const InitDataStateStore = create(set => (
    {
        // Дефолту тут False
        InitDataLoaded: false,
        setInitDataLoaded: state => set({ InitDataLoaded: state }),
    })
)

export default InitDataStateStore

