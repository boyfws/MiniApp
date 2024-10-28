import React, { useState, useEffect } from 'react';
import { Title, List, Modal } from '@telegram-apps/telegram-ui';
import { useHistory } from 'react-router-dom';

import CategoryButtons from '../../components/CategoryButtons/CategoryButtons';
import RestaurantCards from '../../components/RestaurantCards/RestaurantCards';
import Loader from '../../components/Loading/Loading';
import AdressButton from '../../components/AdressButton/AdressButton';
import SearchButton from '../../components/SearchButton/SearchButton';
import ScrollToTopButton from '../../components/ScrollToTopButton/ScrollToTopButton';
import ProfileAvatar from '../../components/ProfileAvatar/ProfileAvatar';

import intersection_checker  from '../../utils/intersection_checker.js';

import './MainPage.css';
import { userId } from '../../telegramInit.js'

import fetchCategories from '../../api/fetchCategories';
import fetchRestaurants from '../../api/fetchRestaurants';
import fetchAdress from '../../api/fetchAdress';

import GetHandleProfileClick from '../../handlers/hadleProfileClick.js';
import GetHandleCardClick from '../../handlers/handleRestCardClick.js';
import GetHandleCategorySelect from '../../handlers/handleCategorySelect.js';
import GetHandleLoadingFinish from '../../handlers/handleLoadingFinish.js';

import ModalMainPage from '../../pages/ModalMainPage/ModalMainPage';

const NUMBER_OF_RESTAURANTS_ON_PAGE = 200;

const MainPage = () => {
  const [categories, setCategories] = useState([]);
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true); // Флаг загрузки
  const [selectedCategories, setSelectedCategories] = useState(new Set())
  const [filteredRestaurants, setFilteredRestaurants] = useState([]); // Новое состояние для фильтрованных ресторанов
  const [showContent, setShowContent] = useState(false); // Чтобы рендерить контент после индикатора
  const [defaultAdress, setDefaultAdress] = useState({});
  const [ScrollPostionY, setScrollPostionY] = useState(0);
  const [AdressLoaded, setAdressLoaded] = useState(false);

  const history = useHistory();

  const handleCardClick = GetHandleCardClick(history, setScrollPostionY);
  const handleProfileClick = GetHandleProfileClick(history, setScrollPostionY);
  const handleCategorySelect = GetHandleCategorySelect(setSelectedCategories);
  const handleLoadingFinish = GetHandleLoadingFinish(setShowContent);

  useEffect(() => {
    setFilteredRestaurants(() => {
      if (selectedCategories.size === 0) {
        return restaurants; 
        }
    
      console.log("Вызвана сортировка");
      return restaurants.filter((restaurant) =>
        intersection_checker(selectedCategories, restaurant.categories)
      );
    });
  }, [selectedCategories, restaurants]); 


  useEffect(() => {
    // Функция для получения данных
    const fetchData = async () => {
      const adress_query = await fetchAdress(userId);
      const categories_query = await fetchCategories(userId);
      if (!adress_query.error && !categories_query.error) {
        setDefaultAdress(adress_query.data);
        setCategories(categories_query.data)
        setAdressLoaded(true);
    };
  }
    fetchData();
  }, []);


useEffect(() => {
  const fetchData = async () => {
    const restaurants_query = await fetchRestaurants(userId, NUMBER_OF_RESTAURANTS_ON_PAGE, defaultAdress);
    if (!restaurants_query.error) {

      const RestaurnatsData = restaurants_query.data.map(restaurant => ({
        ...restaurant, 
        categories: new Set(restaurant.categories) 
      }));

      setRestaurants(RestaurnatsData);
      setFilteredRestaurants(RestaurnatsData);
      if (loading) {
        setLoading(false);
      }
    }
    }
    if (AdressLoaded) {
      fetchData();
    }
  }, [defaultAdress]);


  const handleSearchClick = () => {console.log('Поиск');}

  if (!showContent) {
    return (
    <div className='loading-wrapper' style={{backgroundColor: 'var(--tgui--bg_color)'}}>
        <Loader loading={loading} onFinish={handleLoadingFinish} />
    </div> // Показ сообщения о загрузке, пока данные не получены
    )
  };


  return (
    <div className="main-page-container" 
    style={{
      background: 'var(--tgui--bg_color)',
      padding: 10
    }}>
      <div className={'page-content'}>
        <List className='list'>

            <div className="upper-level-wrapper">

              <ProfileAvatar onClick={handleProfileClick} className="profile-avatar"/>

              <Modal
                header={<Modal.Header/>}
                trigger={<AdressButton defaultAdress={defaultAdress} className="adress-button"/>}
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