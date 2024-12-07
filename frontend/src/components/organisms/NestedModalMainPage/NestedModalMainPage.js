// Css
import "./NestedModalMainPage.css"

// Ext lib
import React from 'react';
import { Modal } from '@telegram-apps/telegram-ui'

// Comp
import NestedModalMainPageContent from "../../molecules/NestedModalMainPageContent/NestedModalMainPageContent";


const NestedModalMainPage = ({InnerModalState, InnerModalRef}) => {

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