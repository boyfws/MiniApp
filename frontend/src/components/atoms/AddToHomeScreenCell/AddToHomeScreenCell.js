// Css
import './AddToHomeScreenCell.css'

// Ext lib
import {Cell} from "@telegram-apps/telegram-ui";


// Utils
import GetAddToHomeScreen from "./utils/AddToHomeScreen";


const AddToHomeScreenCell = ({show}) => {
    // Show отвечает за показ данного элемента
    const AddToHomeScreen = GetAddToHomeScreen()

    return (
        <Cell
            className={`addToHomeScreenCell${show ? "" : "-hidden"}`}
            onClick={AddToHomeScreen}
        >
            Добавить мини приложение на главный экран
        </Cell>
    )

}

export default AddToHomeScreenCell;