import fetchRestaurants from "../api/fetchRestaurants";

const userId = 1 // Мок

const GetLoadRestByAddress = (defAddress, setDefaultRestaurants, RestLoaded, setRestLoaded) => () => {
    const fetchData = async () => {



      const restaurants_query = await fetchRestaurants(userId, defAddress.geometry.coordinates);
      if (!restaurants_query.error) {
  
        const RestaurnatsData = restaurants_query.data.map(restaurant => ({
          ...restaurant, 
          categories: new Set(restaurant.categories) 
        }));
  
        setDefaultRestaurants(RestaurnatsData);
        if (!RestLoaded) {
            setRestLoaded(true);}
      }
    }
    if (Object.keys(defAddress).length !== 0) {
      console.log(defAddress);
      fetchData();
      console.log("Вызвана инициализация ресторанов");
    }
}


export default GetLoadRestByAddress