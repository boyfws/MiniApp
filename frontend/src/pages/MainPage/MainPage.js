import React, { useState, useEffect } from 'react';
import { Title, List, Modal } from '@telegram-apps/telegram-ui';
import { useHistory } from 'react-router-dom';

// Components
import CategoryButtons from '../../components/CategoryButtons/CategoryButtons';
import RestaurantCards from '../../components/RestaurantCards/RestaurantCards';
import Loader from '../../components/Loading/Loading';
import AdressButton from '../../components/AdressButton/AdressButton';
import SearchButton from '../../components/SearchButton/SearchButton';
import ScrollToTopButton from '../../components/ScrollToTopButton/ScrollToTopButton';
import ProfileAvatar from '../../components/ProfileAvatar/ProfileAvatar';
import SearchForm from '../../components/SearchForm/SearchForm';
import ModalMainPage from '../../pages/ModalMainPage/ModalMainPage';

// Design
import './MainPage.css';

// Webhooks
import GetLoadMainPageInitData from '../../webhooks/LoadMainPageInitData'
import GetSortByCategory from '../../webhooks/SortByCategory';
import GetLoadRestByAdress from '../../webhooks/LoadRestByAdress';

// Handlers
import GetHandleProfileClick from '../../handlers/hadleProfileClick';
import GetHandleCardClick from '../../handlers/handleRestCardClick';
import GetHandleCategorySelect from '../../handlers/handleCategorySelect';
import GetHandleLoadingFinish from '../../handlers/handleLoadingFinish';
import GetHandleBackFromSearch from '../../handlers/handleBackFromSearch';
import GetHandleSearchClick from '../../handlers/handleSearchClick';


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

  // Handlers
  const handleCardClick = GetHandleCardClick(history, setScrollPostionY);
  const handleProfileClick = GetHandleProfileClick(history, setScrollPostionY);
  const handleCategorySelect = GetHandleCategorySelect(setSelectedCategories);
  const handleLoadingFinish = GetHandleLoadingFinish(setShowContent);
  const handleBackFromSearch = GetHandleBackFromSearch(setSearchClicked);
  const handleSearchClick = GetHandleSearchClick(setSearchClicked);
  

  // Webhooks
  const LoadMainPageInitData = GetLoadMainPageInitData(
    setDefaultAdress, 
    setAdress_coordinates, 
    setAdresses, 
    setCategories, 
    setAdressLoaded
  );
  const SortByCategory = GetSortByCategory(
    setFilteredRestaurants, 
    selectedCategories, 
    restaurants
  );
  const LoadRestByAdress = GetLoadRestByAdress(
    NUMBER_OF_RESTAURANTS_ON_PAGE, 
    Adress_coordinates, 
    setRestaurants, 
    setFilteredRestaurants, 
    loading, 
    setLoading, 
    AdressLoaded
  );

  // Wil be added soon 
  useEffect(() => {
    console.log(InputValue)
  }, [InputValue]);


  useEffect(SortByCategory, [selectedCategories, restaurants]); 

  useEffect(LoadMainPageInitData, []);

  useEffect(LoadRestByAdress, [defaultAdress]);


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