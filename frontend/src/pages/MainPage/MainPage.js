import React, { useState, useEffect } from 'react';
import { Title, Spinner, Text } from '@telegram-apps/telegram-ui';
import CategoryButtons from '../../components/CategoryButtons/CategoryButtons';
import RestaurantCards from '../../components/RestaurantCards/RestaurantCards';
import Loader from '../../components/Loading/Loading';
import './MainPage.css';
import { userId } from '../../telegramInit.js'

const NUMBER_OF_RESTAURANTS_ON_PAGE = 2000;

const MainPage = () => {
  const [categories, setCategories] = useState([]);
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true); // Флаг загрузки
  const [selectedCategories, setSelectedCategories] = useState(new Set())
  const [filteredRestaurants, setFilteredRestaurants] = useState([]); // Новое состояние для фильтрованных ресторанов
  const [showContent, setShowContent] = useState(false); // Чтобы рендерить контент после индикатора
  


  useEffect(() => {
    setFilteredRestaurants(() => {
      if (selectedCategories.size === 0) {
        return restaurants; 
        }
    
      
      return restaurants.filter((restaurant) =>
        intersection_checker(selectedCategories, restaurant.categories)
      );
    });
  }, [selectedCategories]); 


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

  // Выгружает категорий с бэка (Переписать после)
  const fetchCategoriesFromBackend = (id) => {
    return ['Категория 1', 'Категория 2', 'Категория 3', 'Шашлык', 'Японская кухня', 'Пиво', 'Бургеры', 'Другие'];
  }

  // Выгружает рестораны с бэка (Переписать после)
  const fetchRestaurantsFromBackend = (id, count) => {
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
        tag: Math.random() < 0.2 ? 'Ваше любимоое' : undefined,
        distance: randomDistance,
      });
    }
    return restaurants;
  }

  useEffect(() => {
    // Функция для получения данных
    const fetchData = async () => {
      try {
        const categoriesData = await fetchCategoriesFromBackend(userId); // Запрос категорий
        const restaurantsData = await fetchRestaurantsFromBackend(userId, NUMBER_OF_RESTAURANTS_ON_PAGE); // Запрос ресторанов
        
        const updatedRestaurantsData = restaurantsData.map(restaurant => ({
          ...restaurant, // Копируем все свойства ресторана
          categories: new Set(restaurant.categories) // Преобразуем categories в Set
        }));

        setCategories(categoriesData);
        setRestaurants(updatedRestaurantsData);
        setFilteredRestaurants(updatedRestaurantsData);
        //setTimeout(() => setLoading(false), 3213); // Фича для тестов долого получения данных
        setLoading(false);
        
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    };  
    fetchData(); 
  }, []);

  const handleLoadingFinish = () => {
    setShowContent(true); // Показ основного контента после завершения индикатора
  };

  if (!showContent) {
    return (
    <div className='loading-wrapper'>
        <Loader loading={loading} onFinish={handleLoadingFinish} />
    </div> // Показ сообщения о загрузке, пока данные не получены
    )
  };

  const intersection_checker = (setA, setB) => {
    if (setA.size > setB.size) {
      [setA, setB] = [setB, setA];
    }

    for (let item of setA) {
      if (setB.has(item)) {
        return true; 
      }
    }
    return false; 
  };

  const handleCategorySelect = (category) => {
    // Сначала обновляем выбранные категории
    setSelectedCategories((prevSelectedCategories) => {
      const updatedSelectedCategories = new Set(prevSelectedCategories);
  
      if (updatedSelectedCategories.has(category)) {
        updatedSelectedCategories.delete(category); 
        console.log(`Убрана категория: ${category}`);
      } else {
        updatedSelectedCategories.add(category);
        console.log(`Добавлена категория: ${category}`);
      }
  
      return updatedSelectedCategories;
    });
  };
  

  const handleCardClick = (restaurant) => {
    // Здесь можно добавить логику для перехода на страницу ресторана
    console.log('Переход на страницу ресторана:', restaurant);
  };

// С цветом надписи нужно поработать 
  return (
    <div className="main-page-container">
      <div className={'page-content'}>
        <CategoryButtons categories={categories} onCategorySelect={handleCategorySelect} />

        <Title level="2" weight="1" plain={false} style={{ color: 'black' }}> 
          Рестораны
        </Title>
        <RestaurantCards restaurants={filteredRestaurants} onCardClick={handleCardClick} />
      </div>
    </div>
  );
};

export default MainPage;