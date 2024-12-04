import React, {useState} from 'react';
import { Input, Modal } from '@telegram-apps/telegram-ui'
import "./NestedModalMainPage.css"

import LocationButton from '../../components/LocationButton/LocationButton';
import RecLinesInnerModal from '../../components/RecomendationLinesInnnerModal/RecLinesInnerModal'

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
            style={{backgroundColor: 'var(--tgui--bg_color)'}}>
                <div className='upper_level_wrapper'>
                    <Input status="focused" 
                    header="Input" 
                    placeholder="Write and clean me" 
                    value={seearchString} 
                    onChange={e => SetseearchString(e.target.value)} 
                    />
                    <LocationButton/>
                </div>
                <RecLinesInnerModal recomendations={recomendations}/>

            </div>
        </Modal>

    )

}


export default NestedModalMainPage