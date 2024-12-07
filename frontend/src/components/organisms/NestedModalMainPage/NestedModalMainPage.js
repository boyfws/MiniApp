// Css
import "./NestedModalMainPage.css"

// Ext lib
import React from 'react';
import { Modal } from '@telegram-apps/telegram-ui'

// State
import MainPageModalStore from "../../../state_management/stores/MianPageModalsStateStore";

// Comp
import NestedModalMainPageContent from "../../molecules/NestedModalMainPageContent/NestedModalMainPageContent";


const NestedModalMainPage = ({InnerModalRef}) => {
    const { InnerModalState } = MainPageModalStore()

    return (
        <Modal
        header={<Modal.Header/>}
        open={InnerModalState}
        dismissible={false}
        ref={InnerModalRef}
        >

            <NestedModalMainPageContent/>

        </Modal>

    )

}

export default NestedModalMainPage