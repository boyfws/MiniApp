const GetGetHomeScreenStatus = (setShowAddToHomeScreen) => () => {
    try {
        const tg = window.Telegram.WebApp;
        new Promise(resolve => tg.checkHomeScreenStatus(
            (status) => resolve(status))
        ).then(
            status => {
                setShowAddToHomeScreen((status === 'unknown' || status === 'missed') && tg.isVersionAtLeast(8));
            }
        )
    }
    catch (error) {
        console.log(error);
    }
}

export default GetGetHomeScreenStatus;