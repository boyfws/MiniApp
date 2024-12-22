// Css
import '/DeleteFavRestCell.css'

// Ext lib
import {Cell} from "@telegram-apps/telegram-ui";

// State
import RestStore from '../../../state_management/stores/RestStore'

// Utils
import GetDeleteAllFavRest from "./utils/DeleteAllFavRest";

const DeleteAllFavRestCell = () => {
    const { setDefaultRestaurants, defaultRestaurants } = RestStore();

    const DeleteAllFavRest = GetDeleteAllFavRest(setDefaultRestaurants, defaultRestaurants)
    return (
        <Cell
            className="deleteAllFavRestCell"
            onClick={async () => {await DeleteAllFavRest}}>
            Очистить любимые рестораны
        </Cell>)
}

export default DeleteAllFavRestCell;