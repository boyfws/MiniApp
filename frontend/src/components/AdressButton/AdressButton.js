import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import './AdressButton.css';

const AdressButton = React.forwardRef(({ defaultAdress, onClick }, ref) => {
    return (
        <Button
            size="s"
            mode="filled"
            onClick={onClick}
            className='adress-button'
            ref={ref} // Передаем ref дочернему элементу
        >
            {defaultAdress}
        </Button>
    );
});

export default AdressButton;