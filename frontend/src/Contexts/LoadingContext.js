import React, {createContext, useEffect, useState} from 'react';

const LoadingContext = createContext();


function LoadingContextProvider({ children }) {
    const [RestLoaded, setRestLoaded] = useState(false); // Флаг загрузки
    const [CategoriesLoaded, setCategoriesLoaded] = useState(false);

    const contextValue = {
        RestLoaded,
        setRestLoaded,
        CategoriesLoaded,
        setCategoriesLoaded,
    };

    return (
        <LoadingContext.Provider value={contextValue}>
            {children}
        </LoadingContext.Provider>
    );
}

export { LoadingContext, LoadingContextProvider };