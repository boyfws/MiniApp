const GetHandleGoBackProfilePage = (history) => () => {
    history.push(`/main`);
    window.Telegram.WebApp.BackButton.hide()
}

export default GetHandleGoBackProfilePage;