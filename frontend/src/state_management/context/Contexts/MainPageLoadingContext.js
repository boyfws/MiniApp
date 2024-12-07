import React, {createContext, useEffect, useState} from 'react';

const MainPageLoadingContext = createContext();


function MainPageLoadingContextProvider({ children }) {
    const [RestLoaded, setRestLoaded] = useState(false); // Флаг загрузки
    const [CategoriesLoaded, setCategoriesLoaded] = useState(false);
    const [AddressesLoaded, setAddressesLoaded] = useState(false);

    const contextValue = {
        RestLoaded,
        setRestLoaded,
        CategoriesLoaded,
        setCategoriesLoaded,
        AddressesLoaded,
        setAddressesLoaded,
    };

    return (
        <MainPageLoadingContext.Provider value={contextValue}>
            {children}
        </MainPageLoadingContext.Provider>
    );
}

export { MainPageLoadingContext, MainPageLoadingContextProvider };