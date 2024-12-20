const GetHandleAddressClick = (setModalState, history) => () => {
    setModalState(false);
    history.push("/addAddress")

}

export default GetHandleAddressClick;