//Css
import './AddAddressButton.css'

//Ext lib
import { Button } from "@telegram-apps/telegram-ui";
import React from "react";
import { useHistory } from "react-router-dom";


const AddAddressButton = () => {
    const history = useHistory();

    return (
        <Button
            mode={"outline"}
            className="AddAddressButton"
            onClick={() => history.push("/addAddress")}
        >
            Добавить новый адрес
        </Button>
    )
}

export default AddAddressButton;