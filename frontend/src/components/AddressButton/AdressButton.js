import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import './AdressButton.css';

const getadress = (adress) => {
    const district = adress?.district ?? '';
    const street = adress?.street ?? '';
    const house = adress?.house ?? '';

    if (street) {
        return `ул.${street} д.${house}`;
    }
    else {
        return `${district} райн.`
    }
}

const AddressButton = React.forwardRef(({ defaultAdress, onClick }, ref) => {
    return (
        <Button
            size="s"
            mode="filled"
            onClick={onClick}
            className='adress-button'
            ref={ref} // Передаем ref дочернему элементу
        >
            {getadress(defaultAdress)}
        </Button>
    );
});

export default AddressButton;