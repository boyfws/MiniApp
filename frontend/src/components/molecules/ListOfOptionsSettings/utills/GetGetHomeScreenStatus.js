const GetGetHomeScreenStatus = (setShowAddToHomeScreen) => () => {
    try {
        const tg = window.Telegram.WebApp;
        new Promise(resolve => tg.checkHomeScreenStatus(
            (status) => resolve(status))
        ).then(
            status => {
                console.log(status);
                setShowAddToHomeScreen((status === 'unknown' || status === 'missed') && parseFloat(tg.version) >= 8);
            }
        )
    }
    catch (error) {
        console.log(error);
    }
}

export default GetGetHomeScreenStatus;