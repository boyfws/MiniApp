// Css
import './ModalMainPage.css';

// Ext lib
import React , {useState} from "react";
import {  Modal } from "@telegram-apps/telegram-ui";


// Components
import NestedModalMainPage from '../NestedModalMainPage/NestedModalMainPage.js'
import ModalMainPageContent from "../../molecules/ModalMainPageContent/ModalMainPageContent";


// Учесть, что ласт адрес хранится в локал сторадж 
const ModalMainPage = ({ModalState, modalRef, setModalState, InnerModalRef, InnerModalState, SetInnerModalState}) => {
    const [Addresses, setAddresses] = useState([])

    const handleAddressClick = (address) => {
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

            <ModalMainPageContent
                SetInnerModalState={SetInnerModalState}
                setModalState={setModalState}
            />

            <NestedModalMainPage
            InnerModalState={InnerModalState}
            InnerModalRef={InnerModalRef}/>

        </Modal>
    )
}


export default ModalMainPage