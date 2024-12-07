import { create } from "zustand";

const MainPageModalsStore = create(set => ({
    ModalState: false,
    setModalState: state => set({ModalState: state}),
    InnerModalState: false,
    SetInnerModalState: state => set({InnerModalState: state})

}))

export default MainPageModalsStore