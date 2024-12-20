import fetchAddressRecomFromCoords from "../../../../api/fetchAddressRecomFromCoords";

const GetHandleLocationButtonClick = (SetRecommendations,
                                      SetSnackBarOpen) => async () => {
    const geo_manager = window.Telegram.WebApp.LocationManager;

    if (geo_manager.isAccessRequested && !geo_manager.isAccessGranted) {
        SetSnackBarOpen(true);
        window.Telegram.WebApp.HapticFeedback.notificationOccurred('error')
    } else {
        try {
            window.Telegram.WebApp.HapticFeedback.impactOccurred('medium')
            const result = await new Promise((resolve, reject) => {
                geo_manager.getLocation((result) => {
                    if (result !== null) {
                        resolve(result); // Успешное получение координат
                    } else {
                        reject(new Error("Пользователь не дал доступ")); // Ошибка получения координат
                    }
                });
            });

            const {latitude: lat, longitude: long} = result;

            if (lat !== undefined && long !== undefined) {
                const rec_query = await fetchAddressRecomFromCoords(long, lat);

                if (!rec_query.error) {
                    SetRecommendations(rec_query.data);
                }
            }

        }
        catch (error) {
            console.error('Возникла ошибка получения гео');
        }
    }
};

export default GetHandleLocationButtonClick;