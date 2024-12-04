import { Title, Button, Modal } from "@telegram-apps/telegram-ui";
import AdressLinesInModal from "../../components/AdressLinesInModal/AdressLinesInModal";
import React , {useState} from "react";
import  NestedModalMainPage from '../../pages/NestedModalMainPage/NestedModalMainPage.js'
import './ModalMainPage.css';

// Учесть, что ласт адрес хранится в локал сторадж 
const ModalMainPage = ({Adresses, setAdresses, setDefaultAdress, setModalState, InerModalRef, InnerModalState, SetInnerModalState}) => {

    const handleAdressClick = (address) => {
        console.log("Клик по адресу: ", address);
        setModalState(false)
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
            <Button 
                mode={"outline"} 
                className="AddAddresButton"
                onClick={() => {SetInnerModalState(true)}}
            >
                Нажми меня сученыщ
            </Button>
            <Modal
            header={<Modal.Header/>}
            open={InnerModalState}
            dismissible={true}
            ref={InerModalRef}
            >
                <NestedModalMainPage/>
            </Modal>
        </div>
    );
};


export default ModalMainPage