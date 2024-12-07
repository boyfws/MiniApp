const GetHandleClickOutside = (modalRef, InnerModalRef, SetInnerModalState, setModalState) => (event) => {
    if (InnerModalRef.current && !InnerModalRef.current.contains(event.target)) {
        SetInnerModalState(false)
    }
    if (!InnerModalRef.current) {
        if (modalRef.current && !modalRef.current.contains(event.target)) {
            setModalState(false)
        }
    }
};

export default GetHandleClickOutside;