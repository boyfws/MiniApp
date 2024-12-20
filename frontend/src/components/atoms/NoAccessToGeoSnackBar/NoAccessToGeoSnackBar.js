import { Snackbar } from "@telegram-apps/telegram-ui";

const NoAccessToGeoSnackBar = ({SetSnackBarOpen}) => {
    return (
        <Snackbar
            onClose={() => {SetSnackBarOpen(false)}}
            onClick={(event) => {event.stopPropagation()}}
            after={(
            <Snackbar.Button onClick={() => {
                window.Telegram.WebApp.LocationManager.openSettings();
                SetSnackBarOpen(false);
                }
            }>
                Открыть настройки
            </Snackbar.Button>
        )}>
            Нет доступа к геолокациииииииииииииии
        </Snackbar>
    )
}

export default NoAccessToGeoSnackBar