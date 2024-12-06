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
// Ласт адрес также проикдывается в tg storage 

const GetLoadMainPageInitData =  (SetdefAddress, setCategories, setAdressLoaded) => () => {
    // Функция для получения данных, запускается один раз
    const fetchData = async () => {
      const categories_query = await fetchCategories(userId);
      if (!categories_query.error) {
        SetdefAddress(def_adress);
        setCategories(categories_query.data);

        setAdressLoaded(true);

    };
  }
    fetchData();
    console.log("Вызвана инициализация главной страницы");
}


export default GetLoadMainPageInitData
