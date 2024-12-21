import fetchRestaurants from "../../../api/fetchRestaurants";


const GetLoadRestByAddress = (defAddress, setDefaultRestaurants, RestLoaded, setRestLoaded) => () => {
    const fetchData = async () => {
        const userId = sessionStorage.getItem("userId");


      const restaurants_query = await fetchRestaurants(userId, defAddress.geometry.coordinates);
      if (!restaurants_query.error) {
  
        const RestaurnatsData = restaurants_query.data.map(restaurant => ({
          ...restaurant, 
          category: new Set(restaurant.category)
        }));
  
        setDefaultRestaurants(RestaurnatsData);
        if (!RestLoaded) {
            setRestLoaded(true);}
      }
    }
    console.log("Хук затригерен")
    if (Object.keys(defAddress).length !== 0) {
      console.log(defAddress);
      fetchData();
      console.log("Вызвана инициализация ресторанов");
    }
}


export default GetLoadRestByAddress