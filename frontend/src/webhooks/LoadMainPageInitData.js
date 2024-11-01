import fetchAdress from "../api/fetchAdress";
import fetchCategories from "../api/fetchCategories";
import { userId } from "../telegramInit";

const GetLoadMainPageInitData =  (setDefaultAdress, setAdress_coordinates, setAdresses, setCategories, setAdressLoaded) => () => {
    // Функция для получения данных, запускается один раз
    const fetchData = async () => {
      const adress_query = await fetchAdress(userId);
      const categories_query = await fetchCategories(userId);
      if (!adress_query.error && !categories_query.error) {
        setDefaultAdress(adress_query.data.last_adress.properties);
        setAdress_coordinates(adress_query.data.last_adress.geometry.coordinates);

        setAdresses(adress_query.data.adresses);
        setCategories(categories_query.data);
        setAdressLoaded(true);

    };
  }
    fetchData();
}


export default GetLoadMainPageInitData
