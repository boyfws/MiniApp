//Css
import "./LocationButton.css"

// Ext lib
import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';

// Icon
import Icon24LocationOutline from '../../_icons/Icon24LocationOutline';


const LocationButton = ({}) => {
    let tg_version = parseFloat(window.Telegram.WebApp.version);

    const onClick = () => {}
    return (
        <Button 
        size="m" 
        mode="bezeled" 
        onClick={onClick}
        className={`location-button${tg_version >= 8 ? '' : '-hidden'}`}
        >
            <Icon24LocationOutline/>
        </Button>
    )
}

export default LocationButton