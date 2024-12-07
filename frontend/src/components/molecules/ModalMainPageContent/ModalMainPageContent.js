// Css
import './ModalMainPageContent.css'

// Ext lib
import React from "react";

// State
import MainPageModalsStore from "../../../state_management/stores/MianPageModalsStateStore";

// Comp
import ModalMainPageTitle from "../../atoms/ModalMainPageTitle/ModalMainPageTitle";
import UserAddresses from "../../atoms/UserAddresses/UserAddresses";
import AddAddressButton from "../../atoms/AddAddressButton/AddAddressButton";


const ModalMainPageContent = ({}) => {
    const { SetInnerModalState } = MainPageModalsStore()

    return (
        <div className="modal-main-page">
            <ModalMainPageTitle/>

            <UserAddresses
                className="address-lines-in-modal"
            />

            <AddAddressButton onClick={() => {SetInnerModalState(true)}}/>
        </div>
    )
};

export default ModalMainPageContent;

