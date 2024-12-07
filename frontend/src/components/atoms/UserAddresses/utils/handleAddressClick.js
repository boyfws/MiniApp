const GetHandleAddressClick = (setModalState, setDefAddress) => (address) => {
    setModalState(false)
    setTimeout(setDefAddress(address), 0)
}


export default GetHandleAddressClick