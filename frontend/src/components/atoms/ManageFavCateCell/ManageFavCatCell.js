// Css
import './ManageFavCatCell.css'

// Ext lib
import {Cell} from "@telegram-apps/telegram-ui";

// State
import FavCatModalState from '../../../state_management/stores/FavouriteCategoriesModalState'

const ManageFavCatCell = () => {
    const { setFCModalState } = FavCatModalState();
    return (
        <Cell className="ManageFavCatCell" onClick={() => setFCModalState(true)}>
            Любимые категории
        </Cell>
    )
}

export default ManageFavCatCell;