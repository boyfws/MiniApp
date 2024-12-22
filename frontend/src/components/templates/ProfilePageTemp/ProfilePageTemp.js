
// Ext lib
import {Modal} from "@telegram-apps/telegram-ui";

// Store
import FavCatModalState from '../../../state_management/stores/FavouriteCategoriesModalState'

// Comp
import SettingsProfilePage from "../../organisms/SettingsProfilePage/SettingsProfilePage";
import ModalCatManCont from "../../organisms/ModalCategoryManagCont/ModalCatManCont";


const ProfilePageTemp = ({}) => {
    const { FCModalState } = FavCatModalState();
    
    return (
        <div>
            <SettingsProfilePage/>

            <Modal
                open={FCModalState}
                onOpenChange={(state) => {console.log(state)}}
                dismissible={true}
            >
               <ModalCatManCont/>
            </Modal>
        </div>
    )
}

export default ProfilePageTemp;