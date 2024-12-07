// Ext lib
import React from "react";

// Comp
import HeaderMainPage from "../../organisms/HeaderMainPage/HeaderMainPage";
import MainMainPage from "../../organisms/MainMainPage/MainMainPage";


const MainPageTemp = ({setScrollPositionY, setModalState}) => {
    return (
        <>
            <HeaderMainPage
                setScrollPositionY={setScrollPositionY}
                setModalState={setModalState}
            />

            <MainMainPage setScrollPositionY={setScrollPositionY}/>
        </>
    )
}

export default MainPageTemp;