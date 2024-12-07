import { create } from 'zustand'


const RestStore = create(
    set => ({
        restaurants: [], // Рестораны отобранные по запросу
        setRestaurants: rest => set({ restaurants: rest }),
        filteredRestaurants: [], // Рестораны с учетом поиска и категорий
        setFilteredRestaurants: rest => set({ filteredRestaurants: rest }),
        defaultRestaurants: [], // Все рестораны без фильтраций по категориям и посику
        setDefaultRestaurants: rest => set({ defaultRestaurants: rest }),

    })
)


export default RestStore;