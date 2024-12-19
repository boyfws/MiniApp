import InitDataStateStore from "./state_management/stores/InitDataLoadingState";
import GetinitializeTelegram from "./utils/telegramInit";
import React, {useEffect} from "react";
import App from "./App";

const AppWrapper = ({}) => {
    const {setInitDataLoaded} = InitDataStateStore()

    const initTG = GetinitializeTelegram(setInitDataLoaded);


    useEffect(initTG, [])

    useEffect(() => {
        window.Telegram.WebApp?.LocationManager.init()
    }, [])


    return (
        <App />
    )
}

export default AppWrapper;