import React, { useState, useEffect } from 'react';
import { Title, List, Modal } from '@telegram-apps/telegram-ui';

import CategoryButtons from '../../components/CategoryButtons/CategoryButtons';
import RestaurantCards from '../../components/RestaurantCards/RestaurantCards';
import Loader from '../../components/Loading/Loading';
import AdressButton from '../../components/AdressButton/AdressButton';
import SearchButton from '../../components/SearchButton/SearchButton';
import ScrollToTopButton from '../../components/ScrollToTopButton/ScrollToTopButton';
import ProfileAvatar from '../../components/ProfileAvatar/ProfileAvatar';

import intersection_checker  from '../../utils/intersection_checker.js';
import fetchCategories  from '../../api/fetchCategories.js';
import fetchRestaurants from '../../api/fetchRestaurants.js';

import './MainPage.css';
import { userId } from '../../telegramInit.js'

import ModalMainPage  from '../ModalMainPage/ModalMainPage';

const NUMBER_OF_RESTAURANTS_ON_PAGE = 200;

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


  useEffect(() => {
    // Функция для получения данных
    const fetchData = async () => {
      try {
        const categoriesData = await fetchCategories(userId); // Запрос категорий
        const restaurantsData = await fetchRestaurants(userId, NUMBER_OF_RESTAURANTS_ON_PAGE); // Запрос ресторанов
        
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
    <div className='loading-wrapper' style={{backgroundColor: 'var(--tgui--bg_color)'}}>
        <Loader loading={loading} onFinish={handleLoadingFinish} />
    </div> // Показ сообщения о загрузке, пока данные не получены
    )
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

  const handleSearchClick = () => {console.log('Поиск');}

  const handleProfileClick = () => {console.log('Профиль');}

  const handleAdressClick = (adress) => {console.log('Адрес');}


  return (


    <div className="main-page-container" 
    style={{
      background: 'var(--tgui--bg_color)',
      padding: 10
    }}>
      <div className={'page-content'}>
        <List className='list'>

            <div className="upper-level-wrapper">
              <ProfileAvatar onClick={handleProfileClick} className="profile-button"/>

              <Modal
                header={<Modal.Header/>}
                trigger={<AdressButton defaultAdress="Текущий адрес" className="adress-button"/>}
                >

                <ModalMainPage/>

              </Modal>

              <SearchButton onSearchClick={handleSearchClick} className="search-button"/>
            </div>

          <CategoryButtons categories={categories} onCategorySelect={handleCategorySelect} style={{marginBottom: 0, marginTop: 0}}/>
        </List>

        <Title level="2" weight="1" plain={false} style={{padding: 0}}> 
          Рестораны
        </Title>
        <RestaurantCards restaurants={filteredRestaurants} onCardClick={handleCardClick} />
        <ScrollToTopButton className="scroll-to-top-button"/>
      </div>
    </div>

  );
};

export default MainPage;