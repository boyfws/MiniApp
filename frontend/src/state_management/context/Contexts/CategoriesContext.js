import React, {createContext, useEffect, useState, useContext} from 'react';

const CategoriesContext = createContext();
import { MainPageLoadingContext } from './MainPageLoadingContext';
import InitDataStateStore from '../../stores/InitDataLoadingState';

import GetLoadCateg from "../../utils/GetLoadCateg";


function CategoriesContextProvider({ children }) {
    const {setCategoriesLoaded} = useContext(MainPageLoadingContext);
    const [categories, setCategories] = useState([]);
    const { InitDataLoaded } = InitDataStateStore();

    const LoadCateg = GetLoadCateg(
        setCategories,
        setCategoriesLoaded,
        InitDataLoaded
    )

    useEffect(LoadCateg, [InitDataLoaded]);


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