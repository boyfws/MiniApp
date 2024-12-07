import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import "./LocationButton.css"
import Icon24LocationOutline from '../../../icons/Icon24LocationOutline';


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