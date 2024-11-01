
const GetHandleBackFromSearch = (setSearchClicked) => () => {
    setSearchClicked(false);
    console.log('Назад из поиска');
}

export default GetHandleBackFromSearch