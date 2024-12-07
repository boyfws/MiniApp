//Css
import './AddAddressButton.css'

//Ext lib
import { Button } from "@telegram-apps/telegram-ui";
import React from "react";


const AddAddressButton = ({onClick}) => {
    return (
        <Button
            mode={"outline"}
            className="AddAddressButton"
            onClick={onClick}
        >
            Добавить новый адрес
        </Button>
    )
}

export default AddAddressButton;