const GetHandleClickOutside = (modalRef, setModalState) => (event) => {
    if (modalRef.current && !modalRef.current.contains(event.target)) {
        setModalState(false)
        }

};

export default GetHandleClickOutside;