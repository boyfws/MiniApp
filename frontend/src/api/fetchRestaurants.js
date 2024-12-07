import fetchWithRetry from "./queries/GET_query";
  
  
  // Заглшука для тестов 
  const getRandomCategories = (arr, n) => {
    const result = [];
    const arrCopy = [...arr]; // Создаем копию массива, чтобы не модифицировать оригинальный
  
    for (let i = 0; i < n; i++) {
      const randomIndex = Math.floor(Math.random() * arrCopy.length); // Выбираем случайный индекс
      result.push(arrCopy[randomIndex]); // Добавляем элемент в результат
      arrCopy.splice(randomIndex, 1); // Удаляем элемент, чтобы избежать повторений
    }
  
    return result;
  };


const fetchRestaurants = async (id, coordinates) => {

    const count = 200
    const cat_for_generating_restaurants = ['Категория 1', 'Категория 2', 'Категория 3', 'Шашлык', 'Японская кухня', 'Пиво', 'Бургеры', 'Другие'];
    const baseImageUrl = 'https://i.imgur.com/892vhef.jpeg';
    
    const restaurants = [];
  
    for (let i = 0; i <= count; i++) {
      const randomDistance = (Math.random() * 10).toFixed(1); // Генерация случайного расстояния от 0 до 10 км
      restaurants.push({
        id: i + 1,
        name: `Ресторан ${i + 1}`, // Циклично выбираем имена из массива
        image: baseImageUrl,
        categories: getRandomCategories(cat_for_generating_restaurants, 3),
        tag: i % 10 == 0 ? 'Ваше любимоое' : undefined,
        distance: randomDistance,
      });
    }
    return {data: restaurants, error: false};
  }

export default fetchRestaurants