const GetHandleLoadingFinish = (setShowContent) => () => {
    window.Telegram.WebApp.HapticFeedback.notificationOccurred("success");
    setShowContent(true);
    console.log("Поступила команда показать контент")// Показ основного контента после завершения индикатора
  };


export default GetHandleLoadingFinish