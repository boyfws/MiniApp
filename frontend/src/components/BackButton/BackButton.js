import React from 'react';
import { Button } from "@telegram-apps/telegram-ui";
import { Icon24ChevronLeft  } from "@telegram-apps/telegram-ui/dist/icons/24/chevron_left"
import './BackButton.css';

const BackButton = ({ onBackClick }) => {
    return (
        <Button 
            size="s" 
            mode="bezeled" 
            onClick={onBackClick}
            className='back-button' >
            <Icon24ChevronLeft  className='icon'/>
        </Button>
    );
}

export default BackButton;