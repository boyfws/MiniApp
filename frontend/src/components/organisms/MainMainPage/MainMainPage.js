// Css
import './MainMainPage.css'

// Ext lib
import React from "react";

// Comp
import MainPageTitle from "../../atoms/MainPageTitle/MainPageTitle";
import RestaurantCards from "../../molecules/RestaurantCards/RestaurantCards";
import ScrollToTopButton from "../../molecules/ScrollToTopButton/ScrollToTopButton";

const MainMainPage = ({setScrollPositionY}) => {
    return (
        <>
            <MainPageTitle/>

            <RestaurantCards setScrollPositionY={setScrollPositionY}/>

            <ScrollToTopButton className="scroll-to-top-button"/>
        </>
    )
}


export default MainMainPage;