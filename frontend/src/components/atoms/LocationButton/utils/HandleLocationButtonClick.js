import fetchDefAddressFromCoords from "../../../../api/fetchDefAddressFromCoords";
import sendAddAddress from "../../../../api/sendAddAddress";

const ShowThatErrorOccurred = (setErrorSnackBarOpen) => {
    setErrorSnackBarOpen(true);
    window.Telegram.WebApp.HapticFeedback.notificationOccurred('error')

}

const GetHandleLocationButtonClick = (SetSnackBarOpen,
                                      setDefAddress,
                                      addAddress,
                                      setErrorSnackBarOpen,
                                      history) => async () => {
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
                const rec_query = await fetchDefAddressFromCoords(long, lat);

                if (!rec_query.error) {
                    const user_id = sessionStorage.getItem("userId");
                    const add_address_promise = await sendAddAddress(rec_query.data, user_id);
                    if (!add_address_promise.error) {
                        setDefAddress(rec_query.data)
                        addAddress(rec_query.data)
                        history.push("/main")
                        window.Telegram.WebApp.BackButton.hide()


                    } else {
                        ShowThatErrorOccurred(setErrorSnackBarOpen);
                    }
                } else {
                    ShowThatErrorOccurred(setErrorSnackBarOpen);
                }
            } else {
                ShowThatErrorOccurred(setErrorSnackBarOpen);
            }
        }
        catch (error) {
            console.error('Возникла ошибка получения гео');
        }
    }
};

export default GetHandleLocationButtonClick;