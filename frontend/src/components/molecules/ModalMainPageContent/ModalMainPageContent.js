// Css
import './ModalMainPageContent.css'

// Ext lib
import React from "react";

// State
import defAddressStore from "../../../state_management/stores/DefAddressStore";

// Handlers
import GetHandleAddressClick from "./utils/handleAddressClick";

// Comp
import ModalMainPageTitle from "../../atoms/ModalMainPageTitle/ModalMainPageTitle";
import UserAddresses from "../../atoms/UserAddresses/UserAddresses";
import AddAddressButton from "../../atoms/AddAddressButton/AddAddressButton";


const ModalMainPageContent = ({setModalState, SetInnerModalState}) => {
    const { setDefAddress } = defAddressStore();
    const handleAddressClick = GetHandleAddressClick(setModalState, setDefAddress);

    return (
        <div className="modal-main-page">
            <ModalMainPageTitle/>

            <UserAddresses
                onClick={handleAddressClick}
                className="address-lines-in-modal"
            />

            <AddAddressButton onClick={() => {SetInnerModalState(true)}}/>
        </div>
    )
};

export default ModalMainPageContent;

