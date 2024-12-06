import './ListOfUpperElMainPage.css'

import UpperLevelMainPage from '../UpperLevelMainPage/UpperLevelMainPage'
import CategoryButtons from '../../components/CategoryButtons/CategoryButtons';


// Webhooks
import GetSortByCategory from '../../webhooks/SortByCategory';
import GetLoadCategWhenRestAreAdded from "../../webhooks/GetLoadCategWhenRestAreAdded";

import { LoadingContext } from '../../Contexts/LoadingContext';


import React, { useState, useEffect, useContext } from 'react'
import { List } from '@telegram-apps/telegram-ui'


const ListOfUpperElMainPage = ({
                                   setFilteredRestaurants,
                                   restaurants,
                                   setRestaurants,
                                   setScrollPositionY,
                                   defaultRestaurants,
                                   setModalState
                               }) => {
    const [categories, setCategories] = useState([]);
    const [selectedCategories, setSelectedCategories] = useState(new Set())

    const {setCategoriesLoaded, RestLoaded} = useContext(LoadingContext);


    const SortByCategory = GetSortByCategory(
        setFilteredRestaurants, 
        selectedCategories, 
        restaurants
      );

    const LoadCategWhenRestAreAdded = GetLoadCategWhenRestAreAdded(
        setCategories,
        setCategoriesLoaded,
        RestLoaded
    )

    useEffect(SortByCategory, [selectedCategories, restaurants]);

    useEffect(LoadCategWhenRestAreAdded, [RestLoaded]);


    return (

    <List className='list'>


        <UpperLevelMainPage 
            setRestaurants={setRestaurants}
            setScrollPositionY={setScrollPositionY}
            defaultRestaurants={defaultRestaurants}
            setModalState={setModalState}
        />

        <CategoryButtons 
        categories={categories}
        setSelectedCategories={setSelectedCategories}
        className='category-buttons'
        />


    </List>

    )
}


export default ListOfUpperElMainPage