//Css
import "./LocationButton.css"

// Ext lib
import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';

// Icon
import Icon24LocationOutline from '../../_icons/Icon24LocationOutline';


const LocationButton = ({}) => {
    let tg = window.Telegram.WebApp
    let tg_version = parseFloat(tg.version);
    const showCondition = tg_version >= 8 && tg.LocationManager.isLocationAvailable

    const onClick = () => {}
    return (
        <Button 
        size="m" 
        mode="bezeled" 
        onClick={onClick}
        className={`location-button${showCondition ? '' : '-hidden'}`}
        >
            <Icon24LocationOutline/>
        </Button>
    )
}

export default LocationButton