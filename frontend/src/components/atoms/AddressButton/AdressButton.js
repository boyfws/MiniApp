// Css
import './AdressButton.css';

// Ext lib
import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';

// States
import DefAddressStore from "../../../state_management/stores/DefAddressStore";

// Utils
import prepare_address_for_display from "./utils/prepare_address_for_display";


const AddressButton = React.forwardRef(({ onClick }, ref) => {
    const { DefAddress } = DefAddressStore();

    return (
        <Button
            size="s"
            mode="filled"
            onClick={onClick}
            className='adress-button'
            ref={ref} // Передаем ref дочернему элементу
        >
            {prepare_address_for_display(DefAddress)}
        </Button>
    );
});

export default AddressButton;