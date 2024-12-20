import { Snackbar } from "@telegram-apps/telegram-ui";

const NoAccessToGeoSnackBar = ({SetSnackBarOpen}) => {
    return (
        <Snackbar
            onClose={() => {SetSnackBarOpen(false)}}
            after={(
            <Snackbar.Button onClick={() => {window.Telegram.WebApp.LocationManager.openSettings()}}>
                Открыть настройки
            </Snackbar.Button>
        )}>
            Нет доступа к геолокации
        </Snackbar>
    )
}

export default NoAccessToGeoSnackBar