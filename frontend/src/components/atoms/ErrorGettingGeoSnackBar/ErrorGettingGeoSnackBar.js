import {Snackbar} from "@telegram-apps/telegram-ui";

const ErrorGettingGeoSnackBar = ({setErrorSnackBarOpen}) => {
    return (
        <Snackbar
        onClose={() => setErrorSnackBarOpen(false)}
        onClick={(event) => {event.stopPropagation()}}
        >
            Возникла ошибка попробуйте снова
        </Snackbar>
    )

}

export default ErrorGettingGeoSnackBar;