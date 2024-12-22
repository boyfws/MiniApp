import deleteAllFavUserRest from '../../../../api/deleteAllUserFavRest';

const GetDeleteAllFavRest = (setDefaultRestaurants, defaultRestaurants) => async () => {
    let confirm = await new Promise((resolve) => {
        window.Telegram.WebApp.showConfirm("Вы уверены, что хотите очистить любимые рестораны? Это действие необратимо", (result) => {
            resolve(result);
        });
    });

    if (confirm) {
        const userId = sessionStorage.getItem("userId");
        const responsePromise = Promise.resolve(deleteAllFavUserRest(userId));


        const updatedRestaurants = defaultRestaurants.map((restaurant) => {
            const {tag, ...rest} = restaurant;
            return rest;
        });

        const response = await responsePromise;

        if (!response.error) {
            setDefaultRestaurants(updatedRestaurants);
        }
    }
};

export default GetDeleteAllFavRest;

