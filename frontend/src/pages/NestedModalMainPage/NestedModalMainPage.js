import React, {useState} from 'react';


const NestedModalMainPage = ({InnerModalState, InerModalRef}) => {
    return (
        <Modal
        header={<Modal.Header/>}
        open={InnerModalState}
        dismissible={true}
        ref={InerModalRef}
        >
            <div 
            className='NestedModalMainPage' 
            style={{backgroundColor: 'var(--tgui--bg_color)'}}>
                Привет мой друг, ты кликнул на дичь которая используется для тестов 


            </div>
        </Modal>

    )

}


export default NestedModalMainPage