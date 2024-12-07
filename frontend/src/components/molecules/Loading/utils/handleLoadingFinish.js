const GetHandleLoadingFinish = (setShowContent) => () => {
    setShowContent(true);
    console.log("Поступила команда показать контент")// Показ основного контента после завершения индикатора
  };


export default GetHandleLoadingFinish