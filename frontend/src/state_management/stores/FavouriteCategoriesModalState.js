import { create } from 'zustand';


const FavCatModalState = create(set => (
    {
        FCModalState: false,
        setFCModalState: state => set({ FCModalState: state }),
    })
)


export default FavCatModalState;