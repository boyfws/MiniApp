import fetchWithRetry from "../queries/GET_query";
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));


const fetchCategories = async (id) => {
  await sleep(1000); // Поток "спит" 2 секунды
    return {data: 
      ['Категория 1', 'Категория 2', 'Категория 3', 'Шашлык', 'Японская кухня', 'Пиво', 'Бургеры', 'Другие'],
      error: false};
      
  }

  export default fetchCategories