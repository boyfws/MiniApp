// Css
import '@telegram-apps/telegram-ui/dist/styles.css'; // Глобальные стили из библиотеки

// Ext lib
import { AppRoot } from "@telegram-apps/telegram-ui";
import React, {useEffect, useState} from "react";

// State
import InitDataStateStore from "./state_management/stores/InitDataLoadingState";


import GetinitializeTelegram from "./utils/telegramInit";
import App from "./App";

const AppWrapper = ({}) => {
    const {setInitDataLoaded} = InitDataStateStore()

    const [isDark, setIsDark] = useState(true);
    const [platform, setPlatform] = useState("base");

    const initTG = GetinitializeTelegram(setInitDataLoaded);


    useEffect(() => {
        setIsDark(window.Telegram.WebApp.colorScheme === 'dark');
    }, [])

    useEffect(() => {
        setPlatform(window.Telegram.WebApp.platform)
    }, [])



    useEffect(initTG, [])

    useEffect(() => {
        window.Telegram.WebApp?.LocationManager.init()
    }, [])


    return (
        <AppRoot
            appearance={isDark ? 'dark' : 'light'}
            platform={['macos', 'ios'].includes(platform) ? 'ios' : 'base'}
        >
            <App />
        </AppRoot>
    )
}

export default AppWrapper;