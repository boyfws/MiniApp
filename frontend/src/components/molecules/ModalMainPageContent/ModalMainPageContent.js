// Css
import './ModalMainPageContent.css'


// Ext lib
import React, {useState} from "react";

// Comp
import ModalMainPageTitle from "../../atoms/ModalMainPageTitle/ModalMainPageTitle";
import UserAddresses from "../../atoms/UserAddresses/UserAddresses";
import AddAddressButton from "../../atoms/AddAddressButton/AddAddressButton";


const ModalMainPageContent = ({setModalState, SetInnerModalState}) => {
    const [Addresses, setAddresses] = useState([])

    const handleAddressClick = (address) => {
        console.log("Клик по адресу: ", address);
        setModalState(false)
    }

    return (
        <div className="modal-main-page">
            <ModalMainPageTitle/>

            <UserAddresses
                addresses={Addresses}
                onClick={handleAddressClick}
                className="address-lines-in-modal"
            />

            <AddAddressButton onClick={() => {SetInnerModalState(true)}}/>
        </div>
    )
};

export default ModalMainPageContent;

