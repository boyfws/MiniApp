// Css
import './NestedModalMainPageContent.css'

// Ext lib
import React, {useState} from "react";
import {Input} from "@telegram-apps/telegram-ui";


// Comp
import NestedModalMainPageTitle from "../../atoms/NestedModalMainPageTitle/NestedModalMainPageTitle";
import LocationButton from "../../atoms/LocationButton/LocationButton";
import RecLinesInnerModal from "../../atoms/RecLinesInnnerModal/RecLinesInnerModal";

const NestedModalMainPageContent = ({}) => {
    const [searchString, SetSearchString] = useState("")
    const [recommendations, SetRecommendations] = useState([])


    return (
        <div
            className='NestedModalMainPage'
        >

            <NestedModalMainPageTitle/>

            <div className='upper_level_wrapper'>

                <Input status="focused"
                       placeholder="Write and clean me"
                       value={searchString}
                       onChange={e => SetSearchString(e.target.value)}
                       className={'input_for_address'}
                />
                <LocationButton className='LocationButton'/>

            </div>

            <RecLinesInnerModal recommendations={recommendations}/>
        </div>
    )
}


export default NestedModalMainPageContent