// Api
import verificateInitData from "../api/verificateInitData";

const GetinitializeTelegram = (setInitDataLoaded) => () => {

    async function initializeTelegram() {

        let tg = window.Telegram.WebApp;
        console.log("Начали верифицировать юзера")

        let user_verified = (
            sessionStorage.getItem('userId') !== null &&
            sessionStorage.getItem('access_token') !== null &&
            sessionStorage.getItem('refresh_token') !== null
        )

        if (tg.initData && !user_verified) {
            const verif_res = await verificateInitData(tg.initData)
            if (!verif_res.error) {

                const queryParams = new URLSearchParams(tg.initData);
                const userParam = queryParams.get('user');
                const decodedUser = decodeURIComponent(userParam);
                const userObject = JSON.parse(decodedUser);
                const userId = userObject.id;
                console.log(userId)

                sessionStorage.setItem('userId', userId);
                sessionStorage.setItem('access_token', verif_res.data.access_token)
                sessionStorage.setItem('refresh_token', verif_res.data.refresh_token)
                setInitDataLoaded(true);
            }
        }
        else if (user_verified) {
            setInitDataLoaded(true);
        }
    }

    initializeTelegram();
}

export default GetinitializeTelegram;