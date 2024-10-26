import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import './AdressButton.css';

const AdressButton = ({defaultAdress, openModal}) => {
    return (
        <Button
            size="s"
            mode="filled"
            onClick={openModal}
            className='adress-button'
        >
            {defaultAdress}
        </Button>
    );
};

export default AdressButton