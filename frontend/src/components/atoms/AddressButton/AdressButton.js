import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import './AdressButton.css';

import modificate_address_for_displ from "../../../utils/modificate_address_for_displ";


const AddressButton = React.forwardRef(({ defaultAdress, onClick }, ref) => {
    return (
        <Button
            size="s"
            mode="filled"
            onClick={onClick}
            className='adress-button'
            ref={ref} // Передаем ref дочернему элементу
        >
            {modificate_address_for_displ(defaultAdress)}
        </Button>
    );
});

export default AddressButton;