// Css
import './AddAddressPage.css'

// Ext lib
import React, {useEffect} from "react";
import { useHistory } from "react-router-dom";



const AddAddressPage = () => {
    const history = useHistory();


    const handleGoBack = () => {
        history.push(`/main`);
        window.Telegram.WebApp.BackButton.hide()
    };

    useEffect(() => {

        window.Telegram.WebApp.BackButton.onClick(handleGoBack);
        window.Telegram.WebApp.BackButton.show()

    }, [])


    return (
        <div className="AddAddressPage">

        </div>

    )
}

export default AddAddressPage