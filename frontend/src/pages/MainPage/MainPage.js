import React, { useState, useEffect, useRef, useContext } from 'react';
import { Title } from '@telegram-apps/telegram-ui';
import { useHistory } from 'react-router-dom';


import RestaurantCards from '../../components/organisms/RestaurantCards/RestaurantCards';
import Loader from '../../components/molecules/Loading/Loading';
import ScrollToTopButton from '../../components/atoms/ScrollToTopButton/ScrollToTopButton';
import ModalMainPage from '../../components/templates/ModalMainPage/ModalMainPage';
import ListOfUpperElMainPage from '../../components/templates/ListOfUpperElMainPage/ListOfUpperElMainPage';


// Webhooks
import GetDependency from '../../webhooks/DepBetwDefRestAndRest';
import GetLoadRestByAddress from '../../webhooks/LoadRestByAddress';


import { LoadingContext } from "../../Contexts/LoadingContext";

import DefAddressStore from "../../stores/DefAddressStore";
import RestStore from "../../stores/RestStore";


import './MainPage.css';


const MainPage = () => {
  // Стейты связанные с ресторанами 

  const { setRestaurants, defaultRestaurants, setDefaultRestaurants } = RestStore()


  // Стейты связанные с загрузкой
  const [showContent, setShowContent] = useState(false); // Чтобы рендерить контент после того как все данные загружены

  const { RestLoaded, CategoriesLoaded, setRestLoaded } = useContext(LoadingContext);

  const [ScrollPositionY, setScrollPositionY] = useState(0);


  const { DefAddress, setDefAddress } =  DefAddressStore();

  // Хуки связанные с дефолтным адресом инициализируем на самом высоком уровне

  //  По факту будем доставать из session storage
  useEffect(() => {
        setDefAddress({
            type: 'Feature',
            geometry: {
                type: 'Point',
                coordinates: [37.587914, 55.783954]
            },
            properties: {
                street: 'Поликарпова',
                house: '1',
                district: 'Хорошёвский',
                city: 'Москва'
            }
        })
  }, [])


    useEffect(() => {
//        tg.CloudStorage.setItem("last_address", DefAddress);
    }, [DefAddress]);

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
            setScrollPositionY={setScrollPositionY}
            setModalState={setModalState}
          />

          <Title level="2" weight="1" plain={false} style={{padding: 0}}> 
            Рестораны
          </Title>

          <RestaurantCards 
            setScrollPositionY={setScrollPositionY}
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