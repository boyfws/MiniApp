// Css
import './AddAddressPageContent.css'

// Ext lib
import React, {useState, useEffect} from "react";

// State
import DefAddressStore from "../../../state_management/stores/DefAddressStore";


// Comp
import AddAddressPageTitle from "../../atoms/AddAddressPageTitle/AddAddressPageTitle";
import LocationButton from "../../atoms/LocationButton/LocationButton";
import RecLinesAddAddressPage from "../../atoms/RecLinesAddAddressPage/RecLinesAddAddressPage";
import SearchFormAddress from "../../atoms/SearchFormAddress/SearchFormAddress";

// Utils
import GetLoadAddressRecom from "./utils/LoadAddressRecom";

const AddAddressPageContent = ({}) => {
    const [searchString, SetSearchString] = useState("")
    const [recommendations, SetRecommendations] = useState([])

    const { DefAddress } = DefAddressStore()

    const LoadAddressRecom = GetLoadAddressRecom(SetRecommendations, searchString, DefAddress);

    useEffect(LoadAddressRecom, [searchString])


    return (
        <div
            className='AddAddressPageContent'
        >

            <AddAddressPageTitle/>

            <div className='upper_level_wrapper'>

                <SearchFormAddress
                    ChangeValueInUpperComp={SetSearchString}
                />

                <LocationButton className='LocationButton'/>

            </div>

            <RecLinesAddAddressPage recommendations={recommendations}/>
        </div>
    )
}


export default AddAddressPageContent;