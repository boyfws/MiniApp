// Css
import './LoaderWrapper.css'

// Ext lib
import React, {useContext} from "react";

// State
import {MainPageLoadingContext} from "../../../state_management/context/Contexts/MainPageLoadingContext";

// Handlers
import GetHandleLoadingFinish from './utils/handleLoadingFinish';

//Components
import Loader from "../../molecules/Loading/Loading";


const LoaderWrapper = ({setShowContent}) => {
    const { RestLoaded, CategoriesLoaded, AddressesLoaded } = useContext(MainPageLoadingContext);
    const loading = !(RestLoaded && CategoriesLoaded && AddressesLoaded);

    const onFinish = GetHandleLoadingFinish(setShowContent)

    return (
        <Loader onFinish={onFinish} loading={loading}/>
    )

}

export default LoaderWrapper;