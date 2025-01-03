// Css
import './MainPage.css';

// Ext lib
import React, { useState, useEffect, useRef, useContext } from 'react';

// State
import { MainPageLoadingContext } from "../../state_management/context/Contexts/MainPageLoadingContext";
import DefAddressStore from "../../state_management/stores/DefAddressStore";
import RestStore from "../../state_management/stores/RestStore";
import AddressesStore from "../../state_management/stores/AddressesStore";
import MainPageModalStore from "../../state_management/stores/MianPageModalsStateStore";
import InitDataStateStore from "../../state_management/stores/InitDataLoadingState";


// Webhooks
import GetDependency from './utils/DepBetwDefRestAndRest';
import GetLoadRestByAddress from './utils/LoadRestByAddress';
import GetLoadAddresses from "./utils/LoadAddresses";
import GetLoadDefAddress from "./utils/LoadDefAddress";


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
    const { RestLoaded, setRestLoaded, setAddressesLoaded } = useContext(MainPageLoadingContext);

    const [ScrollPositionY, setScrollPositionY] = useState(0);

    const { SetInnerModalState,  setModalState } = MainPageModalStore()
    const modalRef = useRef(null);
    const InnerModalRef = useRef(null)

    const { InitDataLoaded } = InitDataStateStore()


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

    const LoadAddresses = GetLoadAddresses(
        InitDataLoaded,
        setAddressesLoaded,
        SetAddresses
    )

    const LoadDefAddress = GetLoadDefAddress(
        InitDataLoaded,
        setDefAddress
    )

    //  По факту будем доставать из session storage
    useEffect(LoadDefAddress, [InitDataLoaded])


    useEffect(() => {
//        window.Telegram.WebApp.CloudStorage.setItem("last_address", DefAddress);
    }, [DefAddress]);

    useEffect(Dependency, [defaultRestaurants]);

    useEffect(LoadRestByAddress, [DefAddress]);

    useEffect(() => {
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
        document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    useEffect(LoadAddresses, [InitDataLoaded]);

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
            modalRef={modalRef}
            InnerModalRef={InnerModalRef}
          />

      </div>
    </div>

  );
};

export default MainPage;