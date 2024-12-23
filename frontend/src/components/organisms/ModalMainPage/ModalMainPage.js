// Css
import './ModalMainPage.css';

// Ext lib
import React , {useState} from "react";
import {  Modal } from "@telegram-apps/telegram-ui";

// Store
import MainPageModalStore from "../../../state_management/stores/MianPageModalsStateStore";


// Components
import NestedModalMainPage from '../NestedModalMainPage/NestedModalMainPage.js'
import ModalMainPageContent from "../../molecules/ModalMainPageContent/ModalMainPageContent";


// Учесть, что ласт адрес хранится в локал сторадж 
const ModalMainPage = ({modalRef, InnerModalRef}) => {
    const { ModalState } = MainPageModalStore()

    return (
        
        <Modal
            header={<Modal.Header/>}
            open={ModalState}
            ref={modalRef}
            dismissible={false}
            nested={true}
              >

            <ModalMainPageContent/>

            <NestedModalMainPage
            InnerModalRef={InnerModalRef}/>

        </Modal>
    )
}


export default ModalMainPage