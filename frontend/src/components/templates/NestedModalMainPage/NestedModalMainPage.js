import React, {useState} from 'react';
import { Input, Modal, Title } from '@telegram-apps/telegram-ui'
import "./NestedModalMainPage.css"

import LocationButton from '../../atoms/LocationButton/LocationButton';
import RecLinesInnerModal from '../../molecules/RecLinesInnnerModal/RecLinesInnerModal'

const NestedModalMainPage = ({InnerModalState, InerModalRef}) => {
    const [seearchString, SetseearchString] = useState("")
    const [recomendations, SetRecomendations] = useState([])
    
    return (
        <Modal
        header={<Modal.Header/>}
        open={InnerModalState}
        dismissible={false}
        ref={InerModalRef}
        >
            <div 
            className='NestedModalMainPage' 
            >
                <Title level="2" weight="1" plain={false} style={{padding: 0}}>
                    Добавить адрес
                </Title>

                <div className='upper_level_wrapper'>
                    <Input status="focused" 
                    placeholder="Write and clean me" 
                    value={seearchString} 
                    onChange={e => SetseearchString(e.target.value)}
                    className={'input_for_address'} 
                    />
                    <LocationButton className='LocationButton'/>
                </div>

                <RecLinesInnerModal recomendations={recomendations}/>
            </div>
        </Modal>

    )

}


export default NestedModalMainPage