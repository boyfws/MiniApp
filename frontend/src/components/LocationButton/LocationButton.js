import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import "./LocationButton.css"


const Icon24LocationOutline = ({ ...restProps }) => (
  <svg
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    {...restProps}
  >
    <path
      d="M12 2C8.13401 2 5 5.13401 5 9C5 14.25 12 22 12 22C12 22 19 14.25 19 9C19 5.13401 15.866 2 12 2Z"
      stroke="currentColor"
      strokeWidth="2"
      fill="none"
    />
    <circle cx="12" cy="9" r="3" fill="currentColor" />
  </svg>
);


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