import { Title } from "@telegram-apps/telegram-ui";
import AdressLinesInModal from "../../components/AdressLinesInModal/AdressLinesInModal";
import React from "react";
import './ModalMainPage.css';

// Учесть, что ласт адрес хранится в локал сторадж 
const ModalMainPage = ({Adresses, setAdresses}) => {

    const handleAdressClick = (address) => {
        console.log("Клик по адресу: ", address);
    }

    return (
        <div className="modal-main-page">
            <Title level="2" weight="1" plain={false} style={{padding: 0}}> 
                Мои адреса
            </Title>
            <AdressLinesInModal
                    adresses={Adresses}
                    onClick={handleAdressClick}
                    className="adress-lines-in-modal"
            />
        </div>
    );
};


export default ModalMainPage