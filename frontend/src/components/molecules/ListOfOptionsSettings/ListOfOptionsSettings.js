
//  Ext lib
import React, {useEffect, useState} from "react";
import { Divider } from "@telegram-apps/telegram-ui";


// Comp
import AddToHomeScreenCell from '../../atoms/AddToHomeScreenCell/AddToHomeScreenCell'
import DeleteAllFavRestCell from "../../atoms/DeleteAllFavRestCell/DeleteAllFavRestCell";
import ManageFavCatCell from '../../atoms/ManageFavCateCell/ManageFavCatCell'

// Utils
import GetGetHomeScreenStatus from './utills/GetGetHomeScreenStatus'


const ListOfOptionsSettings = () => {
    const [showAddToHomeScreen, setShowAddToHomeScreen] = useState(false)

    const GetHomeScreenStatus = GetGetHomeScreenStatus(setShowAddToHomeScreen)

    useEffect(GetHomeScreenStatus, [])

    return (
        <div>
            <ManageFavCatCell/>
            <DeleteAllFavRestCell/>
            {showAddToHomeScreen && (<Divider/>)}
            <AddToHomeScreenCell show={showAddToHomeScreen}/>
        </div>
    )

}

export default ListOfOptionsSettings;