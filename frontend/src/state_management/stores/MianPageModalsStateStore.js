import { create } from "zustand";

const MainPageModalsStore = create(set => ({
    ModalState: false,
    setModalState: state => set({ModalState: state}),

}))

export default MainPageModalsStore