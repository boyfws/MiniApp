import { create } from 'zustand';


const FavCatStore = create(set => (
    {
        FavCat: false,
        setFavCat: favcat => set({ FavCat: favcat }),
    })
)


export default FavCatStore;