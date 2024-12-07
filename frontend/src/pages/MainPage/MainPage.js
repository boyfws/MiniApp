// Css
import './MainPage.css';

// Ext lib
import React, { useState, useEffect, useRef, useContext } from 'react';

// State
import { MainPageLoadingContext } from "../../state_management/context/Contexts/MainPageLoadingContext";
import DefAddressStore from "../../state_management/stores/DefAddressStore";
import RestStore from "../../state_management/stores/RestStore";
import AddressesStore from "../../state_management/stores/AddressesStore";


// Webhooks
import GetDependency from './utils/DepBetwDefRestAndRest';
import GetLoadRestByAddress from './utils/LoadRestByAddress';
import GetLoadAddressesWhenRestAreLoaded from "./utils/LoadAddressesWhenRestAreLoaded";


// Comp
import LoaderWrapper from "../../components/templates/LoaderWrapper/LoaderWrapper.js";
import MainPageTemp from "../../components/templates/MainPageTemp/MainPageTemp";
import ModalMainPage from '../../components/organisms/ModalMainPage/ModalMainPage';
import GetHandleClickOutside from "./utils/hadleClickOutside";


const MainPage = () => {

    const { setRestaurants, defaultRestaurants, setDefaultRestaurants } = RestStore()
    const { DefAddress, setDefAddress } =  DefAddressStore();
    const { SetAddresses } = AddressesStore();

    // Сейты связанные с загрузкой
    const [showContent, setShowContent] = useState(false); // Чтобы рендерить контент после того как все данные загружены
    const { RestLoaded, setRestLoaded, CategoriesLoaded, setAddressesLoaded } = useContext(MainPageLoadingContext);

    const [ScrollPositionY, setScrollPositionY] = useState(0);


    const [ModalState, setModalState] = useState(false)
    const [InnerModalState, SetInnerModalState] = useState(false)
    const modalRef = useRef(null);
    const InnerModalRef = useRef(null)


    // Хуки связанные с дефолтным адресом инициализируем на самом высоком уровне
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

    const LoadAddressesWhenRestAreLoaded = GetLoadAddressesWhenRestAreLoaded(
        RestLoaded,
        setAddressesLoaded,
        SetAddresses
    )


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

    useEffect(Dependency, [defaultRestaurants]);

    useEffect(LoadRestByAddress, [DefAddress]);

    useEffect(() => {
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
        document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    useEffect(LoadAddressesWhenRestAreLoaded, [
        RestLoaded
    ]);

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