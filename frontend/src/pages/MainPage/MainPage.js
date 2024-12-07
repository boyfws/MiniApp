// Css
import './MainPage.css';

// Ext lib
import React, { useState, useEffect, useRef, useContext } from 'react';

// State
import { LoadingContext } from "../../state_management/context/Contexts/LoadingContext";
import DefAddressStore from "../../state_management/stores/DefAddressStore";
import RestStore from "../../state_management/stores/RestStore";


// Webhooks
import GetDependency from './utils/DepBetwDefRestAndRest';
import GetLoadRestByAddress from './utils/LoadRestByAddress';


// Comp
import LoaderWrapper from "../../components/templates/LoaderWrapper/LoaderWrapper.js";
import MainPageTemp from "../../components/templates/MainPageTemp/MainPageTemp";
import ModalMainPage from '../../components/organisms/ModalMainPage/ModalMainPage';
import GetHandleClickOutside from "./utils/hadleClickOutside";


const MainPage = () => {

    const { setRestaurants, defaultRestaurants, setDefaultRestaurants } = RestStore()
    const { DefAddress, setDefAddress } =  DefAddressStore();

    // Сейты связанные с загрузкой
    const [showContent, setShowContent] = useState(false); // Чтобы рендерить контент после того как все данные загружены
    const { RestLoaded, setRestLoaded } = useContext(LoadingContext);

    const [ScrollPositionY, setScrollPositionY] = useState(0);


    const [ModalState, setModalState] = useState(false)
    const [InnerModalState, SetInnerModalState] = useState(false)
    const modalRef = useRef(null);
    const InnerModalRef = useRef(null)


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


    const handleClickOutside = GetHandleClickOutside(
        modalRef,
        InnerModalRef,
        SetInnerModalState,
        setModalState)

  
    useEffect(Dependency, [defaultRestaurants]);

    useEffect(LoadRestByAddress, [DefAddress]);

    useEffect(() => {
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
        document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);


    if (!showContent) {
        return (
            <LoaderWrapper setShowContent={setShowContent}/>
        )
    }

  return (
    <div className="main-page-container">
      <div className={'page-content'}>

          <MainPageTemp setModalState={setModalState} setScrollPositionY={setScrollPositionY}/>

          <ModalMainPage
            ModalState={ModalState}
            modalRef={modalRef}
            setModalState={setModalState}
            InnerModalRef={InnerModalRef}
            InnerModalState={InnerModalState}
            SetInnerModalState={SetInnerModalState}
          />

      </div>
    </div>

  );
};

export default MainPage;