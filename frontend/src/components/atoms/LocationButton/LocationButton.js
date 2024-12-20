//Css
import "./LocationButton.css"

// Ext lib
import React, { useState } from 'react';
import { Button } from '@telegram-apps/telegram-ui';

// Icon
import Icon24LocationOutline from '../../_icons/Icon24LocationOutline';

// Handlers
import GetHandleLocationButtonClick from "./utils/HandleLocationButtonClick";

// Components
import NoAccessToGeoSnackBar from "../NoAccessToGeoSnackBar/NoAccessToGeoSnackBar";


const LocationButton = ({SetRecommendations}) => {
    const [SnackBarOpen,  SetSnackBarOpen] = useState(false);

    let tg = window.Telegram.WebApp
    let tg_version = parseFloat(tg.version);
    const showCondition = tg_version >= 8 && tg.LocationManager.isLocationAvailable

    const HandleLocationButtonClick = GetHandleLocationButtonClick(
        SetRecommendations,
        SetSnackBarOpen)

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

        </Button>
    )
}

export default LocationButton