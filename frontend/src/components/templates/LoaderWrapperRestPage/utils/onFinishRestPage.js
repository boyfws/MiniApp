const onFinishRestPage = (setShowContent) => () =>  {
    setShowContent(true);
    console.log("Выполнилась команда показать контент на фронте");
}

export default onFinishRestPage;