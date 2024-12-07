import fetchRestaurantsSearch from "../../../../api/fetchRestaurantsSearch";

const userId = 1 // Мок 


// Добавить логику для работы с redux для получения дефолтного адреса 
const GetLoadRestFromSearch = (defAddress, InputValue, setRestaurants) => () => {
    const fetchData = async () => {

        const restaurants_query = await fetchRestaurantsSearch(userId, defAddress.geometry.coordinates, InputValue);

        if (!restaurants_query.error) {

            const RestaurnatsData = restaurants_query.data.map(restaurant => ({
                ...restaurant, 
                categories: new Set(restaurant.categories) 
            }));
            setRestaurants(RestaurnatsData);
        }
        
    }
    if (InputValue !== "") {
        fetchData()
    }
};



export default GetLoadRestFromSearch