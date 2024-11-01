import fetchRestaurants from "../api/fetchRestaurants";
import { userId } from "../telegramInit";

const GetLoadRestByAdress = (num, Adress_coordinates, setDefaultRestaurants, AdressLoaded, loading, setLoading) => () => {
    const fetchData = async () => {
      const restaurants_query = await fetchRestaurants(userId, num, Adress_coordinates);
      if (!restaurants_query.error) {
  
        const RestaurnatsData = restaurants_query.data.map(restaurant => ({
          ...restaurant, 
          categories: new Set(restaurant.categories) 
        }));
  
        setDefaultRestaurants(RestaurnatsData);
        if (loading) {
          setLoading(false);}
      }
      }
      if (AdressLoaded) {
        fetchData();
        console.log("Вызвана инициализация ресторанов");
      }
}


export default GetLoadRestByAdress