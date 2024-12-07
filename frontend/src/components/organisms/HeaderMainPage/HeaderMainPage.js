// Css
import './HeaderMainPage.css'

// Ext lib
import { List } from '@telegram-apps/telegram-ui'

// Components
import UpperLevelInHeaderMainPage from '../../molecules/UpperLevelInHeaderMainPage/UpperLevelInHeaderMainPage'
import CategoryButtons from '../../molecules/CategoryButtons/CategoryButtons';


const HeaderMainPage = ({setScrollPositionY, setModalState}) => {
    return (
        <List className='list'>

            <UpperLevelInHeaderMainPage
                setScrollPositionY={setScrollPositionY}
                setModalState={setModalState}
            />

            <CategoryButtons className='category-buttons'/>

        </List>
    )
}


export default HeaderMainPage