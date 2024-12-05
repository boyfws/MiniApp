import fetchAdress from "../api/fetchAdress";
import fetchCategories from "../api/fetchCategories";


const userId = 1 // Мок 

const def_adress = {
  type: 'Feature',
  geometry: {
    type: 'Point',
    coordinates: [37.587914, 55.783954]
  },
  properties: {
    street: 'Поликарпова',
    house: '1',
    district: 'Хорошёвский',
    city: 'Москва'
  }
}
// Ласт адрес достается из локал стораджа на самом деле 

const GetLoadMainPageInitData =  (setDefaultAdress, setAdress_coordinates, setAdresses, setCategories, setAdressLoaded) => () => {
    // Функция для получения данных, запускается один раз
    const fetchData = async () => {
      const adress_query = await fetchAdress(userId);
      const categories_query = await fetchCategories(userId);
      if (!adress_query.error && !categories_query.error) {
        setDefaultAdress(def_adress.properties);
        setAdress_coordinates(def_adress.geometry.coordinates);

        setAdresses(adress_query.data);
        setCategories(categories_query.data);
        setAdressLoaded(true);

    };
  }
    fetchData();
    console.log("Вызвана инициализация главной страницы");
}


export default GetLoadMainPageInitData
