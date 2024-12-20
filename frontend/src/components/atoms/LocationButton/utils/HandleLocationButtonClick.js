import fetchAddressRecomFromCoords from "../../../../api/fetchAddressRecomFromCoords";

const GetHandleLocationButtonClick = (SetRecommendations) => async () => {
    try {
        const geo_manager = window.Telegram.WebApp.LocationManager;

        const result = await new Promise((resolve, reject) => {
            geo_manager.getLocation((result) => {
                if (result !== null) {
                    resolve(result); // Успешное получение координат
                } else {
                    reject(new Error("Пользователь не дал доступ")); // Ошибка получения координат
                }
            });
        });

        const { latitude: lat, longitude: long } = result;

        if (lat !== undefined && long !== undefined) {
            const rec_query = await fetchAddressRecomFromCoords(long, lat);

            if (!rec_query.error) {
                SetRecommendations(rec_query.data);
            }
        }

    } catch (error) {
        console.error('Возникла ошибка получения гео');
    }
};

export default GetHandleLocationButtonClick;