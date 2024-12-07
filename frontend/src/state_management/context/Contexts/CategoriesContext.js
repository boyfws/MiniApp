import React, {createContext, useEffect, useState, useContext} from 'react';

const CategoriesContext = createContext();

import { MainPageLoadingContext } from './MainPageLoadingContext';
import GetLoadCategWhenRestAreAdded from "../../utils/GetLoadCategWhenRestAreAdded";


function CategoriesContextProvider({ children }) {
    const {setCategoriesLoaded, RestLoaded} = useContext(MainPageLoadingContext);
    const [categories, setCategories] = useState([]);

    const LoadCategWhenRestAreAdded = GetLoadCategWhenRestAreAdded(
        setCategories,
        setCategoriesLoaded,
        RestLoaded
    )

    useEffect(LoadCategWhenRestAreAdded, [RestLoaded]);



    const contextValue = {
        categories
    };

    return (
        <CategoriesContext.Provider value={contextValue}>
            {children}
        </CategoriesContext.Provider>
    );
}

export { CategoriesContext, CategoriesContextProvider };