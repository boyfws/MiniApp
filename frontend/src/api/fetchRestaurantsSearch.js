// Заглушка для тестов 
import fetchRestaurants from "./fetchRestaurants"


const fetchRestaurantsSearch = (id, coordinates, searchQuery) => {
    console.log("Вызван запрос по строчке " + searchQuery)
    return fetchRestaurants(id, 10)
}

export default fetchRestaurantsSearch