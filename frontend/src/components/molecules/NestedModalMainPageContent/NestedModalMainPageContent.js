// Css
import './NestedModalMainPageContent.css'

// Ext lib
import React, {useState, useEffect} from "react";

// State
import DefAddressStore from "../../../state_management/stores/DefAddressStore";


// Comp
import NestedModalMainPageTitle from "../../atoms/NestedModalMainPageTitle/NestedModalMainPageTitle";
import LocationButton from "../../atoms/LocationButton/LocationButton";
import RecLinesInnerModal from "../../atoms/RecLinesInnnerModal/RecLinesInnerModal";
import SearchFormAddress from "../../atoms/SearchFormAddress/SearchFormAddress";

// Utils
import GetLoadAddressRecom from "./utils/LoadAddressRecom";

const NestedModalMainPageContent = ({}) => {
    const [searchString, SetSearchString] = useState("")
    const [recommendations, SetRecommendations] = useState([])

    const { DefAddress } = DefAddressStore()

    const LoadAddressRecom = GetLoadAddressRecom(SetRecommendations, searchString, DefAddress);

    useEffect(LoadAddressRecom, [searchString])




    return (
        <div
            className='NestedModalMainPage'
        >

            <NestedModalMainPageTitle/>

            <div className='upper_level_wrapper'>

                <SearchFormAddress
                    ChangeValueInUpperComp={SetSearchString}
                />

                <LocationButton className='LocationButton'/>

            </div>

            <RecLinesInnerModal recommendations={recommendations}/>
        </div>
    )
}


export default NestedModalMainPageContent