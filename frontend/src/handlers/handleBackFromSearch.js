
const GetHandleBackFromSearch = (setSearchClicked, setRestaurants, defaultRestaurants) => () => {
    setSearchClicked(false);
    setRestaurants(defaultRestaurants);
    console.log('Назад из поиска');
}

export default GetHandleBackFromSearch