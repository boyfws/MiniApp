import React, { useState, useEffect, useRef } from 'react';
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
import GetDependency from '../../webhooks/DepBetwDefRestAndRest';
import GetLoadRestFromSearch from '../../webhooks/GetNewRestFromSearch';

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
  const [selectedCategories, setSelectedCategories] = useState(new Set())

  const [restaurants, setRestaurants] = useState([]); // Состояние для показываемых на данный момент рестораноов
  const [filteredRestaurants, setFilteredRestaurants] = useState([]); // Новое состояние для фильтрованных ресторанов
  const [defaultRestaurants, setDefaultRestaurants] = useState([]); // Состояние для дефолтных ресторанов на данный момент 

  const [loading, setLoading] = useState(true); // Флаг загрузки
  const [showContent, setShowContent] = useState(false); // Чтобы рендерить контент после индикатора

  const [defaultAdress, setDefaultAdress] = useState({});
  const [Adress_coordinates, setAdress_coordinates] = useState({});
  const [Adresses, setAdresses] = useState([]);
  const [AdressLoaded, setAdressLoaded] = useState(false);

  const [ScrollPostionY, setScrollPostionY] = useState(0);

  const [searchClicked, setSearchClicked] = useState(false);
  const [InputValue, setInputValue] = useState('');
  const [ModalState, setModalState] = useState(false)

  const [InnerModalState, SetInnerModalState] = useState(false)
  const modalRef = useRef(null);
  const InerModalRef = useRef(null)


  const history = useHistory();

  // Handlers
  const handleCardClick = GetHandleCardClick(history, setScrollPostionY);
  const handleProfileClick = GetHandleProfileClick(history, setScrollPostionY);
  const handleCategorySelect = GetHandleCategorySelect(setSelectedCategories);
  const handleLoadingFinish = GetHandleLoadingFinish(setShowContent);
  const handleBackFromSearch = GetHandleBackFromSearch(
    setSearchClicked, 
    setRestaurants, 
    defaultRestaurants
  );
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
    setDefaultRestaurants, 
    AdressLoaded, 
    loading,
    setLoading
  );

  const Dependency = GetDependency(
    setRestaurants, 
    defaultRestaurants
  );
  
  const LoadRestFromSearch = GetLoadRestFromSearch(
    InputValue, 
    Adress_coordinates, 
    setRestaurants
  );

  useEffect(LoadMainPageInitData, []);

  useEffect(LoadRestByAdress, [defaultAdress]);

  useEffect(Dependency, [defaultRestaurants]);

  useEffect(SortByCategory, [selectedCategories, restaurants]); 

  useEffect(LoadRestFromSearch, [InputValue]);


  const CloseFirstModal = (event) => {
    if (modalRef.current && !modalRef.current.contains(event.target)) {
      setModalState(false)
    }
  }


  const handleClickOutside = (event) => {
    if (InerModalRef.current && !InerModalRef.current.contains(event.target)) {
      SetInnerModalState(false)
    }
    if (!InerModalRef.current) {
      CloseFirstModal(event)
    }
  }

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);


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
                  <AdressButton 
                    defaultAdress={defaultAdress} 
                    className='adress-button'
                    onClick={() => {setModalState(true)}}/>



                  <SearchButton onSearchClick={handleSearchClick} className='search-button' />

                </div>

                <div className={`search${searchClicked ? '' : '-hidden'}`}>
                  <SearchForm 
                  handleBack={handleBackFromSearch} 
                  ChangeValueInMainPage={setInputValue}/>
                </div>

              </div>

              <CategoryButtons 
              categories={categories} 
              onCategorySelect={handleCategorySelect} 
              style={{marginBottom: 0, marginTop: 0}} 
              className='category-buttons'/>


          </List>

          <Title level="2" weight="1" plain={false} style={{padding: 0}}> 
            Рестораны
          </Title>
          <RestaurantCards restaurants={filteredRestaurants} onCardClick={handleCardClick} />
          <ScrollToTopButton className="scroll-to-top-button"/>


        <ModalMainPage
        ModalState={ModalState} 
        modalRef={modalRef} 
        Adresses={Adresses}
        setAdresses={setAdresses}
        setDefaultAdress={setDefaultAdress}
        setModalState={setModalState}
        InerModalRef={InerModalRef}
        InnerModalState={InnerModalState}
        SetInnerModalState={SetInnerModalState}/>
      </div>
    </div>

  );
};

export default MainPage;