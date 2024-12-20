//Css
import './AddAddressButton.css'

//Ext lib
import { Button } from "@telegram-apps/telegram-ui";
import React from "react";
import { useHistory } from "react-router-dom";

// State
import MainPageModalsStore from "../../../state_management/stores/MianPageModalsStateStore"

// Utils
import GetHandleAddAddressClick from "./utils/handleAddAddressClick";


const AddAddressButton = () => {
    const { setModalState } = MainPageModalsStore()
    const history = useHistory();

    const handleAddAddressClick = GetHandleAddAddressClick(setModalState, history);

    return (
        <Button
            mode={"outline"}
            className="AddAddressButton"
            onClick={handleAddAddressClick}
        >
            Добавить новый адрес
        </Button>
    )
}

export default AddAddressButton;