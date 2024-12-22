//Css
import "./LocationButton.css"

// Ext lib
import React, { useState } from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import {useHistory} from "react-router-dom";

// States
import DefAddressStore from "../../../state_management/stores/DefAddressStore";
import AddressesStore from "../../../state_management/stores/AddressesStore";


// Handlers
import GetHandleLocationButtonClick from "./utils/HandleLocationButtonClick";

// Components
import NoAccessToGeoSnackBar from "../NoAccessToGeoSnackBar/NoAccessToGeoSnackBar";
import ErrorGettingGeoSnackBar from "../ErrorGettingGeoSnackBar/ErrorGettingGeoSnackBar";

// Icon
import Icon24LocationOutline from '../../_icons/Icon24LocationOutline';


const LocationButton = ({}) => {
    const { setDefAddress } = DefAddressStore()
    const { addAddress } = AddressesStore()
    const history = useHistory()

    const [SnackBarOpen,  SetSnackBarOpen] = useState(false);
    const [ErrorSnackBarOpen, setErrorSnackBarOpen] = useState(false);

    let tg = window.Telegram.WebApp
    let tg_version = parseFloat(tg.version);
    const showCondition = tg_version >= 8 && tg.LocationManager.isLocationAvailable

    const HandleLocationButtonClick = GetHandleLocationButtonClick(
        SetSnackBarOpen,
        setDefAddress,
        addAddress,
        setErrorSnackBarOpen,
        history)

    return (
        <Button 
        size="m" 
        mode="bezeled" 
        onClick={async () => {await HandleLocationButtonClick()}}
        className={`location-button${showCondition ? '' : '-hidden'}`}
        >
            <Icon24LocationOutline/>

            {SnackBarOpen && (
                <NoAccessToGeoSnackBar SetSnackBarOpen={SetSnackBarOpen}/>
            )}

            {ErrorSnackBarOpen && (
                <ErrorGettingGeoSnackBar setErrorSnackBarOpen={setErrorSnackBarOpen}/>
            )}

        </Button>
    )
}

export default LocationButton