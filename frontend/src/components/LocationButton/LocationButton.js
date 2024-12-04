import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import "./LocationButton.css"


const Icon24LocationOutline = ({ ...restProps }) => (
    <svg width="24" height="24" fill="none" xmlns="http://www.w3.org/2000/svg" {...restProps}>
      <path
        d="M12 2C12.5523 2 13 2.44772 13 3V12C13 12.5523 12.5523 13 12 13C11.4477 13 11 12.5523 11 12V3C11 2.44772 11.4477 2 12 2Z"
        fill="currentColor"
      />
      <circle cx="12" cy="18" r="2" fill="currentColor" />
      <path
        d="M12 21C14.7614 21 17 18.7614 17 16H7C7 18.7614 9.23858 21 12 21Z"
        fill="currentColor"
      />
    </svg>
  );


const LocationButton = ({onClick}) => {
    return (
        <Button 
        size="m" 
        mode="bezeled" 
        onClick={onClick}
        className='location-button' >
            <Icon24LocationOutline/>
        </Button>
    )
}

export default LocationButton