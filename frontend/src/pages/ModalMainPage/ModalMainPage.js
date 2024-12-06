import { Title, Button, Modal } from "@telegram-apps/telegram-ui";
import AdressLinesInModal from "../../components/AdressLinesInModal/AdressLinesInModal";
import React , {useState} from "react";
import  NestedModalMainPage from '../../pages/NestedModalMainPage/NestedModalMainPage.js'
import './ModalMainPage.css';

// Учесть, что ласт адрес хранится в локал сторадж 
const ModalMainPage = ({ModalState, modalRef, setModalState, InerModalRef, InnerModalState, SetInnerModalState, SetdefAddress}) => {
    const [Addresses, setAddresses] = useState([])

    const handleAdressClick = (address) => {
        console.log("Клик по адресу: ", address);
        setModalState(false)
    }

    return (
        
        <Modal
            header={<Modal.Header/>}
            open={ModalState}
            ref={modalRef}
            dismissible={false}
            nested={true}
              >

            <div className="modal-main-page">
                <Title level="2" weight="1" plain={false} style={{padding: 0}}> 
                    Мои адреса
                </Title>
                <AdressLinesInModal
                    adresses={Addresses}
                    onClick={handleAdressClick}
                    className="adress-lines-in-modal"
                />
                <Button 
                    mode={"outline"} 
                    className="AddAddresButton"
                    onClick={() => {SetInnerModalState(true)}}
                >
                Добавить новый адрес
                </Button>
            <NestedModalMainPage
            InnerModalState={InnerModalState}
            InerModalRef={InerModalRef}/>
            </div>
        </Modal>
    )
}


export default ModalMainPage