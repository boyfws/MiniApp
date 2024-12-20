const GetHandleAddAddressClick = (setModalState, history) => () => {
    setModalState(false);
    history.push("/addAddress")

}

export default GetHandleAddAddressClick;