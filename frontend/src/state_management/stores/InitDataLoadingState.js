import { create } from 'zustand';


const InitDataStateStore = create(set => (
    {
        // Дефолту тут False
        InitDataLoaded: true,
        setInitDataLoaded: state => set({ InitDataLoaded: state }),
    })
)

export default InitDataStateStore

