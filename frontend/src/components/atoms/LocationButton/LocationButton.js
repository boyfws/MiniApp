//Css
import "./LocationButton.css"

// Ext lib
import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';

// Icon
import Icon24LocationOutline from '../../_icons/Icon24LocationOutline';


const LocationButton = ({onClick}) => {
    return (
        <Button 
        size="m" 
        mode="bezeled" 
        onClick={onClick}
        className='location-button'
        >
            <Icon24LocationOutline/>
        </Button>
    )
}

export default LocationButton