import './ListOfUpperElMainPage.css'

import UpperLevelMainPage from '../../organisms/UpperLevelMainPage/UpperLevelMainPage'
import CategoryButtons from '../../molecules/CategoryButtons/CategoryButtons';



import { List } from '@telegram-apps/telegram-ui'


const ListOfUpperElMainPage = ({
                                   setScrollPositionY,
                                   setModalState
                               }) => {

    return (

    <List className='list'>

        <UpperLevelMainPage 
            setScrollPositionY={setScrollPositionY}
            setModalState={setModalState}
        />

        <CategoryButtons className='category-buttons'/>

    </List>

    )
}


export default ListOfUpperElMainPage