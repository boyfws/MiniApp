import React, { useState, useEffect, useRef, useContext } from 'react';
import { Title } from '@telegram-apps/telegram-ui';
import { useHistory } from 'react-router-dom';


import RestaurantCards from '../../components/RestaurantCards/RestaurantCards';
import Loader from '../../components/Loading/Loading';
import ScrollToTopButton from '../../components/ScrollToTopButton/ScrollToTopButton';
import ModalMainPage from '../../pages/ModalMainPage/ModalMainPage';
import ListOfUpperElMainPage from '../../components/ListOfUpperElMainPage/ListOfUpperElMainPage';


// Webhooks
import GetDependency from '../../webhooks/DepBetwDefRestAndRest';
import GetLoadRestByAddress from '../../webhooks/LoadRestByAddress';


import { DefAddressContext } from "../../Contexts/DefAddressContext";
import { LoadingContext } from "../../Contexts/LoadingContext";


import './MainPage.css';


const MainPage = () => {
  // Стейты связанные с ресторанами 
  const [restaurants, setRestaurants] = useState([]); // Рестораны отобранные по запросу
  const [filteredRestaurants, setFilteredRestaurants] = useState([]); // Рестораны с учетом поиска и категорий
  const [defaultRestaurants, setDefaultRestaurants] = useState([]); // Все рестораны без фильтраций по категориям и посику


  // Стейты связанные с загрузкой
  const [showContent, setShowContent] = useState(false); // Чтобы рендерить контент после того как все данные загружены

  const { RestLoaded, CategoriesLoaded, setRestLoaded } = useContext(LoadingContext);

  const [ScrollPositionY, setScrollPositionY] = useState(0);


  const { DefAddress } = useContext(DefAddressContext);


  const history = useHistory();


  // Работа с модальными окнами
  const [ModalState, setModalState] = useState(false)
  const [InnerModalState, SetInnerModalState] = useState(false)
  const modalRef = useRef(null);
  const InnerModalRef = useRef(null)


  const Dependency = GetDependency(
    setRestaurants, 
    defaultRestaurants
  );


  const LoadRestByAddress = GetLoadRestByAddress(
      DefAddress,
      setDefaultRestaurants,
      RestLoaded,
      setRestLoaded
  );

  
  useEffect(Dependency, [defaultRestaurants]);

  useEffect(LoadRestByAddress, [DefAddress]);


  const CloseFirstModal = (event) => {
    if (modalRef.current && !modalRef.current.contains(event.target)) {
      setModalState(false)
    }
  }


  const handleClickOutside = (event) => {
    if (InnerModalRef.current && !InnerModalRef.current.contains(event.target)) {
      SetInnerModalState(false)
    }
    if (!InnerModalRef.current) {
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
    <div className='loading-wrapper'>
        <Loader loading={!(RestLoaded && CategoriesLoaded)} setShowContent={setShowContent} />
    </div> // Показ сообщения о загрузке, пока данные не получены
    )
  }


  return (
    <div className="main-page-container">
      <div className={'page-content'}>


          <ListOfUpperElMainPage
            setFilteredRestaurants={setFilteredRestaurants}

            restaurants={restaurants} 
            setRestaurants={setRestaurants}

            setScrollPositionY={setScrollPositionY}
            defaultRestaurants={defaultRestaurants}
            setModalState={setModalState}

          />

          <Title level="2" weight="1" plain={false} style={{padding: 0}}> 
            Рестораны
          </Title>

          <RestaurantCards 
            restaurants={filteredRestaurants}
            setScrollPositionY={setScrollPositionY}
            history={history}
          />

          <ScrollToTopButton className="scroll-to-top-button"/>


          <ModalMainPage
            ModalState={ModalState}
            modalRef={modalRef}
            setModalState={setModalState}
            InerModalRef={InnerModalRef}
            InnerModalState={InnerModalState}
            SetInnerModalState={SetInnerModalState}
          />
      </div>
    </div>

  );
};

export default MainPage;