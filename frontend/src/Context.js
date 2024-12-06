import React, {createContext, useEffect, useState} from 'react';

const Context = createContext();


function ContextProvider({ children }) {
    const [DefAddress, SetDefAddress] = useState({});
//    const tg = window.Telegram.WebApp

    // По факту будем доставать из клоуд сторадж
    useEffect(() => {
        SetDefAddress({
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


    const contextValue = {
        DefAddress,
        SetDefAddress,
    };

    return (
        <Context.Provider value={contextValue}>
            {children}
        </Context.Provider>
    );
}

export { Context, ContextProvider };