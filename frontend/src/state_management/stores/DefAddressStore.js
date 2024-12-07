import { create } from 'zustand';


const DefAddressStore = create(set => (
    {
        DefAddress: {},
        setDefAddress: address => set({ DefAddress: address }),
    })
)


export default DefAddressStore;