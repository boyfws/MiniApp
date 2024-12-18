import fetchAddresses from "../../../api/fetchAddresses";

// Загружает адреса пользователя, если рестораны загружены
const GetLoadAddresses = (InitDataLoaded, setAddressesLoaded, SetAddresses) => () => {
    const fetchData = async () => {
        const user_id = sessionStorage.getItem("userId");
        const addresses_query = await fetchAddresses(user_id);
        if (!addresses_query.error) {
            SetAddresses(addresses_query.data);
            setAddressesLoaded(true);
        }

    }
    if (InitDataLoaded) {
        fetchData();
        console.log("Загружены адреса")
    }

}

export default GetLoadAddresses