import fetchAddressFromRec from "../../../../api/fetchAddressFromRec";
import sendAddAddress from "../../../../api/sendAddAddress"

const GetHandleAddressRecClick = (setModalState,
                                  history,
                                  addAddress,
                                  setDefAddress) => async (recom) => {
    setModalState(false)
    history.push("/main");
    window.Telegram.WebApp.BackButton.hide()

    const new_address_query = await fetchAddressFromRec(
        recom.full_name,
        recom?.city ?? null,
        recom?.region ?? null,
        recom?.street ?? null,
        recom?.district ?? null,
        recom?.house ?? null
        )
        if (!new_address_query.error) {
            setDefAddress(new_address_query.data)
            addAddress(new_address_query.data)
            let userId = sessionStorage.getItem("userId")
            await sendAddAddress(new_address_query.data, userId)

        }

}

export default GetHandleAddressRecClick;