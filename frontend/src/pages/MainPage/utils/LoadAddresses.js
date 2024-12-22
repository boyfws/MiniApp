import fetchAddresses from "../../../api/fetchAddresses";

// Загружает адреса пользователя, если рестораны загружены
const GetLoadAddresses = (InitDataLoaded, setAddressesLoaded, addAddress) => () => {
    const fetchData = async () => {
        const user_id = sessionStorage.getItem("userId");
        const addresses_query = await fetchAddresses(user_id);
        if (!addresses_query.error) {
            for (let element of addresses_query.data) {
                addAddress(element);
            }
            setAddressesLoaded(true);
        }

    }
    if (InitDataLoaded) {
        fetchData();
    }

}

export default GetLoadAddresses