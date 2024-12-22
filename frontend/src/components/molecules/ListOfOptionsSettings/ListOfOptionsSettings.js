
//  Ext lib
import React, {useEffect, useState} from "react";
import { Divider } from "@telegram-apps/telegram-ui";


// Comp
import AddToHomeScreenCell from '../../atoms/AddToHomeScreenCell/AddToHomeScreenCell'
import DeleteAllFavRestCell from "../../atoms/DeleteAllFavRestCell/DeleteAllFavRestCell";

// Utils
import GetGetHomeScreenStatus from './utills/GetGetHomeScreenStatus'


const ListOfOptionsSettings = () => {
    const [showAddToHomeScreen, setShowAddToHomeScreen] = useState(false)

    const GetHomeScreenStatus = GetGetHomeScreenStatus(showAddToHomeScreen)

    useEffect(GetHomeScreenStatus, [])

    return (
        <div>
            <DeleteAllFavRestCell/>
            {showAddToHomeScreen && (<Divider/>)}
            <AddToHomeScreenCell show={showAddToHomeScreen}/>
        </div>
    )

}

export default ListOfOptionsSettings;