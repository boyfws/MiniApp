const GetHandleSearchClick = (setSearchClicked) => () => {
    window.Telegram.WebApp.HapticFeedback.impactOccurred('medium')
    setSearchClicked(true);
    console.log('Активирован поиск');
}


export default GetHandleSearchClick