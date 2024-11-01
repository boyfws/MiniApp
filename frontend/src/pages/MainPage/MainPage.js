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
import SearchForm from '../../components/SearchForm/SearchForm';

import intersection_checker  from '../../utils/intersection_checker';

import './MainPage.css';
import { userId } from '../../telegramInit.js'

import fetchCategories from '../../api/fetchCategories';
import fetchRestaurants from '../../api/fetchRestaurants';
import fetchAdress from '../../api/fetchAdress';

import GetHandleProfileClick from '../../handlers/hadleProfileClick';
import GetHandleCardClick from '../../handlers/handleRestCardClick';
import GetHandleCategorySelect from '../../handlers/handleCategorySelect';
import GetHandleLoadingFinish from '../../handlers/handleLoadingFinish';
import GetHandleBackFromSearch from '../../handlers/handleBackFromSearch';

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
  const [Adress_coordinates, setAdress_coordinates] = useState({});
  const [Adresses, setAdresses] = useState([]);
  const [ScrollPostionY, setScrollPostionY] = useState(0);
  const [AdressLoaded, setAdressLoaded] = useState(false);
  const [searchClicked, setSearchClicked] = useState(false);
  const [InputValue, setInputValue] = useState('');

  const history = useHistory();

  const handleCardClick = GetHandleCardClick(history, setScrollPostionY);
  const handleProfileClick = GetHandleProfileClick(history, setScrollPostionY);
  const handleCategorySelect = GetHandleCategorySelect(setSelectedCategories);
  const handleLoadingFinish = GetHandleLoadingFinish(setShowContent);
  const handleBackFromSearch = GetHandleBackFromSearch(setSearchClicked);


  useEffect(() => {
    console.log(InputValue)
  }, [InputValue]);


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
}, []);


useEffect(() => {
  const fetchData = async () => {
    const restaurants_query = await fetchRestaurants(userId, NUMBER_OF_RESTAURANTS_ON_PAGE, Adress_coordinates);
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


  const handleSearchClick = () => {
    console.log('Поиск');
    setSearchClicked(true);
  }

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
              <div className={`upper-level${searchClicked ? '-hidden' : ''}`}>
                <ProfileAvatar onClick={handleProfileClick} className='profile-avatar'/>

                <Modal
                  header={<Modal.Header/>}
                  trigger={<AdressButton defaultAdress={defaultAdress} className='adress-button'/>}
                  >

                  <ModalMainPage/>

                </Modal>

                <SearchButton onSearchClick={handleSearchClick} className='search-button' />

              </div>

              <div className={`search${searchClicked ? '' : '-hidden'}`}>
                <SearchForm 
                handleBack={handleBackFromSearch} 
                ChangeValueInMainPage={setInputValue}/>
              </div>

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