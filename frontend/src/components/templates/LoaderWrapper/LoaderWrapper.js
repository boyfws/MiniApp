// Css
import './LoaderWrapper.css'

// Ext lib
import React from "react";

//Components
import Loader from "../../molecules/Loading/Loading";

const LoaderWrapper = ({setShowContent}) => {
    return (
        <div className='loading-wrapper'>
            <Loader setShowContent={setShowContent} />
        </div> // Показ сообщения о загрузке, пока данные не получены
    )

}

export default LoaderWrapper;