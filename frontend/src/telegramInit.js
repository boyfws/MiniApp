// State
import InitDataStateStore from './state_management/stores/InitDataLoadingState';

// Api
import verificateInitData from "./api/verificateInitData";

async function initializeTelegram() {
    const { setInitDataLoaded } = InitDataStateStore()

    let tg = window.Telegram.WebApp;
    if (tg.initData && !(
        sessionStorage.getItem('userId') !== null && 
        sessionStorage.getItem('access_token') !== null && 
        sessionStorage.getItem('refresh_token') !== null 
        )){
        const verif_res = await verificateInitData(tg.initData)
        if (!verif_res.error) {

            const queryParams = new URLSearchParams(tg.initData);
            const userParam = queryParams.get('user');
            const decodedUser = decodeURIComponent(userParam);
            const userObject = JSON.parse(decodedUser);
            const userId = userObject.id; 

            sessionStorage.setItem('userId', userId);
            sessionStorage.setItem('access_token', verif_res.data.access_token)
            sessionStorage.setItem('refresh_token', verif_res.data.refresh_token)
            setInitDataLoaded(true);
        }
    }
}

await initializeTelegram()