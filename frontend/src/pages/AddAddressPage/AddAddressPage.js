import './AddAddressPage.css'
import React, {useEffect} from "react";



const AddAddressPage = () => {
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