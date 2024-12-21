const GetHandleGoBack = (history) => () => {
    history.push(`/main`);
    window.Telegram.WebApp.BackButton.hide();
};

export default GetHandleGoBack;