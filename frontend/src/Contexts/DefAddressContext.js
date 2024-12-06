import React, {createContext, useEffect, useState} from 'react';

const DefAddressContext = createContext();


function DefAddressProvider({ children }) {
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
        <DefAddressContext.Provider value={contextValue}>
            {children}
        </DefAddressContext.Provider>
    );
}

export { DefAddressContext, DefAddressProvider };