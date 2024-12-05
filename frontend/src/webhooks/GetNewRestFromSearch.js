import fetchRestaurantsSearch from "../api/fetchRestaurantsSearch";

const userId = 1 // Мок 

const GetLoadRestFromSearch = (InputValue, Adress_coordinates, setRestaurants) => () => { 
    const fetchData = async () => {

        const restaurants_query = await fetchRestaurantsSearch(userId, Adress_coordinates, InputValue);

        if (!restaurants_query.error) {

            const RestaurnatsData = restaurants_query.data.map(restaurant => ({
                ...restaurant, 
                categories: new Set(restaurant.categories) 
            }));
            setRestaurants(RestaurnatsData);
        }
        
    }
    if (InputValue != "") {
        fetchData()
    };
};



export default GetLoadRestFromSearch