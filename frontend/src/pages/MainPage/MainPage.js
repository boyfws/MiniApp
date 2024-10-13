import React, { useState } from 'react';
import { Title } from '@telegram-apps/telegram-ui';
import CategoryButtons from '../../components/CategoryButtons/CategoryButtons';
import RestaurantCards from '../../components/RestaurantCards/RestaurantCards';

const MainPage = () => {
  const [selectedCategory, setSelectedCategory] = useState(null);

  const categories = ['Категория 1', 'Категория 2', 'Категория 3', 'Шашлык', 'Японская кухня', 'Пиво', 'Бургеры', 'Другие'];
  const restaurants = [
    {
      id: 1, 
      name: 'Ресторан 1',
      tag: 'Горячее место',
      image: 'https://i.imgur.com/892vhef.jpeg',
      distance: "1.5",
    },
    { id: 2,
      name: 'Ресторан 2',
      image: 'https://i.imgur.com/892vhef.jpeg',
      distance: "2.5",
    },
    {
      id: 3,
      name: 'Ресторан 3',
      image: 'https://i.imgur.com/892vhef.jpeg',
      distance: "3.5",
    }
  ];

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    // Здесь можно добавить логику для фильтрации ресторанов по выбранной категории
  };

  const handleCardClick = (restaurant) => {
    // Здесь можно добавить логику для перехода на страницу ресторана
    console.log('Переход на страницу ресторана:', restaurant);
  };
// С цветом надписи нужно поработать 
  return (
    <div className="main-page-container">
      <div className="main-page">
        <CategoryButtons categories={categories} onCategorySelect={handleCategorySelect} />

        <Title level="2" weight="1" plain={false} style={{ color: 'black' }}> 
          Рестораны
        </Title>
        <RestaurantCards restaurants={restaurants} onCardClick={handleCardClick} />
      </div>
    </div>
  );
};

export default MainPage;