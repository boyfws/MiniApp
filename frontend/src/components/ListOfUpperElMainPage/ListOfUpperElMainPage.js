import './ListOfUpperElMainPage.css'

import UpperLevelMainPage from '../UpperLevelMainPage/UpperLevelMainPage'
import CategoryButtons from '../../components/CategoryButtons/CategoryButtons';


// Webhooks
import GetSortByCategory from '../../webhooks/SortByCategory';


import React, { useState, useEffect } from 'react'
import { List } from '@telegram-apps/telegram-ui'


const ListOfUpperElMainPage = ({
                                   setFilteredRestaurants,
                                   restaurants,
                                   setRestaurants,
                                   setScrollPositionY,
                                   defaultRestaurants,
                                   setModalState,
                               }) => {
    const [categories, setCategories] = useState([]);
    const [selectedCategories, setSelectedCategories] = useState(new Set())


    const SortByCategory = GetSortByCategory(
        setFilteredRestaurants, 
        selectedCategories, 
        restaurants
      );

    useEffect(SortByCategory, [selectedCategories, restaurants]); 


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