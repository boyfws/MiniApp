import fetchRestaurants from "../api/fetchRestaurants";
import { userId } from "../telegramInit";

const GetLoadRestByAdress = (num, Adress_coordinates, setRestaurants, setFilteredRestaurants, loading, setLoading, AdressLoaded) => () => {
    const fetchData = async () => {
      const restaurants_query = await fetchRestaurants(userId, num, Adress_coordinates);
      if (!restaurants_query.error) {
  
        const RestaurnatsData = restaurants_query.data.map(restaurant => ({
          ...restaurant, 
          categories: new Set(restaurant.categories) 
        }));
  
        setRestaurants(RestaurnatsData);
        setFilteredRestaurants(RestaurnatsData);
        if (loading) {
          setLoading(false);
        }
      }
      }
      if (AdressLoaded) {
        fetchData();
      }
}


export default GetLoadRestByAdress