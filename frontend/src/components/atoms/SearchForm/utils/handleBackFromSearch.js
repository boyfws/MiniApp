
const GetHandleBackFromSearch = (setSearchClicked, setRestaurants, defaultRestaurants) => () => {
    window.Telegram.WebApp.HapticFeedback.impactOccurred('medium')
    setSearchClicked(false);
    setRestaurants(defaultRestaurants);
    console.log('Назад из поиска');
}

export default GetHandleBackFromSearch