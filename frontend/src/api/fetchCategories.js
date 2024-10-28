import fetchWithRetry from "../queries/GET_query";


const fetchCategories = (id) => {
  console.log("Вызвано api категории")
    return {data: 
      ['Категория 1', 'Категория 2', 'Категория 3', 'Шашлык', 'Японская кухня', 'Пиво', 'Бургеры', 'Другие'],
      error: false};
      
  }

  export default fetchCategories